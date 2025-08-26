
import pandas as pd
import requests
import re
import os

# Importa a aplicação e a base de dados da sua estrutura
from helpers.application import app
from helpers.database import db

# --- FUNÇÃO 1: CARGA DO CENSO ---
def carregar_dados_censo():
    """Carrega os dados do Censo a partir dos ficheiros CSV para a base de dados."""
    print("\n--- Iniciando carga dos dados do Censo Escolar ---")
    files_to_process = [
        'microdados_ed_basica_2023.csv',
        'microdados_ed_basica_2024.csv'
    ]
    table_name = 'instituicoes'
    # Lista completa de colunas desejadas
    colunas_desejadas = [
        "NO_REGIAO", "CO_REGIAO", "NO_UF", "SG_UF", "CO_UF", "NO_MUNICIPIO", 
        "CO_MUNICIPIO", "NO_MESORREGIAO", "NO_MICRORREGIAO", "NO_ENTIDADE", 
        "CO_ENTIDADE", "QT_MAT_BAS", "QT_MAT_INF", "QT_MAT_FUND", "QT_MAT_MED", 
        "QT_MAT_EJA", "QT_MAT_EJA_FUND", "QT_MAT_ESP", "QT_MAT_BAS_EAD", 
        "QT_MAT_FUND_INT", "QT_MAT_MED_INT"
    ]

    for file_path in files_to_process:
        print(f"Processando ficheiro: {file_path}...")
        if not os.path.exists(file_path):
            print(f"AVISO: Ficheiro não encontrado. A saltar: {file_path}")
            continue

        match = re.search(r'_(\d{4})\.csv', file_path)
        if not match:
            print(f"AVISO: Não foi possível extrair o ano de '{file_path}'.")
            continue
        year = int(match.group(1))

        try:
            df = pd.read_csv(file_path, sep=';', encoding='latin1', usecols=colunas_desejadas, low_memory=False)
            df['ano'] = year
            df.to_sql(table_name, db.engine, if_exists='append', index=False)
            print(f"SUCESSO: {len(df)} registos de {file_path} carregados.")
        except Exception as e:
            print(f"ERRO ao processar {file_path}: {e}")

# --- FUNÇÃO 2: CARGA DE LOCALIDADES (IBGE) ---
def carregar_localidades_ibge():
    """Carrega os dados de UFs, Municípios, etc., a partir da API do IBGE."""
    print("\n--- Iniciando carga das localidades via API do IBGE ---")
    
    endpoints = {
        "ufs": "https://servicodados.ibge.gov.br/api/v1/localidades/estados",
        "municipios": "https://servicodados.ibge.gov.br/api/v1/localidades/municipios",
        "mesorregioes": "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes",
        "microrregioes": "https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes",
    }

    for table_name, url in endpoints.items():
        print(f"Buscando dados para: {table_name}...")
        try:
            response = requests.get(f"{url}?orderBy=nome")
            response.raise_for_status()
            dados_json = response.json()
            
            df = pd.json_normalize(dados_json)
            
            # Aplica lógicas específicas de mapeamento de colunas
            if table_name == 'ufs':
                mapa = {'id': 'id', 'sigla': 'sigla', 'nome': 'nome', 'regiao.id': 'regiao_id', 'regiao.sigla': 'regiao_sigla', 'regiao.nome': 'regiao_nome'}
                df = df[list(mapa.keys())].rename(columns=mapa)
            elif table_name == 'municipios':
                mapa = {
                    'id': 'id', 'nome': 'nome', 'microrregiao.id': 'microrregiao_id', 'microrregiao.nome': 'microrregiao_nome',
                    'microrregiao.mesorregiao.id': 'mesorregiao_id', 'microrregiao.mesorregiao.nome': 'mesorregiao_nome',
                    'microrregiao.mesorregiao.UF.id': 'uf_id', 'microrregiao.mesorregiao.UF.sigla': 'uf_sigla',
                    'microrregiao.mesorregiao.UF.nome': 'uf_nome', 'microrregiao.mesorregiao.UF.regiao.id': 'regiao_id',
                    'microrregiao.mesorregiao.UF.regiao.sigla': 'regiao_sigla', 'microrregiao.mesorregiao.UF.regiao.nome': 'regiao_nome'
                }
                df = df[list(mapa.keys())].rename(columns=mapa)
            else: # Para mesorregiões e microrregiões
                df.columns = df.columns.str.replace('.', '_', regex=False)

            df.to_sql(table_name, db.engine, if_exists='replace', index=False)
            print(f"SUCESSO: Tabela '{table_name}' criada/atualizada com {len(df)} registos.")
        except Exception as e:
            print(f"ERRO ao carregar dados para '{table_name}': {e}")

# --- EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    
    db.init_app(app)

    with app.app_context():
        print("======================================================")
        print("INICIALIZANDO E POPULANDO A BASE DE DADOS POSTGRESQL...")
        print("======================================================")
        
        # Importa todos os modelos para que o `create_all` os reconheça
        from models.instituicao import Instituicao
        # Se criar modelos para as localidades, importe-os aqui também.

        print("A apagar tabelas antigas (se existirem)...")
        db.drop_all()
        
        print("A criar novas tabelas...")
        db.create_all()
        
        # Executa as cargas de dados
        carregar_dados_censo()
        carregar_localidades_ibge()
        
        print("\n🎉 Processo de inicialização da base de dados finalizado!")
