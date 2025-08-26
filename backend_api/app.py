from helpers.application import app, api
from helpers.database import db
from helpers.cors import cors

from resources.instituicao import InstituicoesResource, InstituicaoResource

# Inicializa as extensões com a aplicação
db.init_app(app)
cors.init_app(app, resources={r"/*": {"origins": "*"}}) # Permite todas as origens

# Adiciona os resources (endpoints) à API
api.add_resource(InstituicoesResource, '/instituicoes')
api.add_resource(InstituicaoResource, '/instituicoes/<int:id>/<int:ano>')

if __name__ == '__main__':
    with app.app_context():
        # Cria as tabelas no banco de dados se elas não existirem
        db.create_all()
    app.run(debug=True, port=5000)
