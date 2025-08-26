from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError

from models.instituicao import Instituicao, InstituicaoSchema
from backend_api.helpers.database import db

# Schema para usar na validação
instituicao_schema = InstituicaoSchema()
instituicao_update_schema = InstituicaoSchema(partial=True) 

# Função auxiliar para serializar um objeto Instituicao para um dicionário
def serialize_instituicao(inst):
    return {
        'id': inst.CO_ENTIDADE,
        'nome': inst.NO_ENTIDADE,
        'municipio': inst.NO_MUNICIPIO,
        'uf_codigo': inst.CO_UF,
        'uf_nome': inst.NO_UF,
        'uf_sigla': inst.SG_UF,
        'qt_mat_inf': inst.QT_MAT_INF,
        'qt_mat_fund': inst.QT_MAT_FUND,
        'ano': inst.ano
    }

# --- Resource para uma coleção de instituições (GET, POST) ---
class InstituicoesResource(Resource):
    def get(self):
        # Parâmetros da URL para paginação e filtro
        uf_sigla = request.args.get('uf')
        try:
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 20))
        except ValueError:
            return {'message': 'Os parâmetros page e per_page devem ser números inteiros.'}, 400

        if not uf_sigla:
            return {'message': "O parâmetro 'uf' é obrigatório."}, 400

        print(f"Buscando instituições para a UF: {uf_sigla.upper()} (página {page}, {per_page} por página)")
        
        try:
            # Busca TODOS os registros para o estado
            instituicoes_2023 = db.session.query(Instituicao).filter_by(SG_UF=uf_sigla.upper(), ano=2023).all()
            instituicoes_2024 = db.session.query(Instituicao).filter_by(SG_UF=uf_sigla.upper(), ano=2024).all()
            
            todas_instituicoes = instituicoes_2023 + instituicoes_2024
            
            # Aplica a paginação na lista combinada
            total_items = len(todas_instituicoes)
            start_index = (page - 1) * per_page
            end_index = start_index + per_page
            paginated_list = todas_instituicoes[start_index:end_index]

            # Constrói a resposta com os dados paginados e metadados
            response = {
                "items": [serialize_instituicao(inst) for inst in paginated_list],
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total_items": total_items,
                    "total_pages": (total_items + per_page - 1) // per_page # Divisão de teto
                }
            }
            
            return jsonify(response)

        except Exception as e:
            print(f"ERRO INTERNO NO SERVIDOR: {e}")
            return {'message': 'Ocorreu um erro interno no servidor.'}, 500

    def post(self):
        json_data = request.get_json()
        try:
            data = instituicao_schema.load(json_data)
        except ValidationError as err:
            return {'message': 'Erro de validação', 'errors': err.messages}, 400

        instituicao_existente = db.session.query(Instituicao).filter_by(CO_ENTIDADE=data['CO_ENTIDADE'], ano=data['ano']).first()
        if instituicao_existente:
            return {'message': 'Uma instituição com este ID e ano já existe.'}, 409

        nova_instituicao = Instituicao(**data)
        db.session.add(nova_instituicao)
        db.session.commit()

        return serialize_instituicao(nova_instituicao), 201


# --- (GET, PUT, DELETE) ---
class InstituicaoResource(Resource):
    def get(self, id, ano):
        instituicao = db.session.query(Instituicao).filter_by(CO_ENTIDADE=id, ano=ano).first()
        if not instituicao:
            return {'message': 'Instituição não encontrada'}, 404
        return serialize_instituicao(instituicao)

    def put(self, id, ano):
        instituicao = db.session.query(Instituicao).filter_by(CO_ENTIDADE=id, ano=ano).first()
        if not instituicao:
            return {'message': 'Instituição não encontrada'}, 404
            
        json_data = request.get_json()
        try:
            data = instituicao_update_schema.load(json_data)
        except ValidationError as err:
            return {'message': 'Erro de validação', 'errors': err.messages}, 400
        
        for key, value in data.items():
            setattr(instituicao, key, value)
        
        db.session.commit()
        return serialize_instituicao(instituicao)

    def delete(self, id, ano):
        instituicao = db.session.query(Instituicao).filter_by(CO_ENTIDADE=id, ano=ano).first()
        if not instituicao:
            return {'message': 'Instituição não encontrada'}, 404
            
        db.session.delete(instituicao)
        db.session.commit()
        return {}, 204
