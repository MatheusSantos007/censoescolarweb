import requests
import pandas as pd
from sqlalchemy import create_engine

def buscar_e_carregar_microrregioes(db_engine, table_name):
    """
    Busca os dados de todas as microrregiões do Brasil via API do IBGE
    e carrega em uma tabela do banco de dados.
    """
    # URL da API de Microrregiões do IBGE
    API_URL = "https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes?orderBy=nome"
    
    print(f"--- Buscando dados das Microrregiões na API do IBGE ---")
    print(f"URL: {API_URL}")

    try:
        # 1. Fazer a requisição para a API
        response = requests.get(API_URL)
        response.raise_for_status()  # Lança um erro se a requisição falhar
        
        # 2. Converter a resposta JSON em uma lista de dicionários
        dados_json = response.json()
        print(f"✅ {len(dados_json)} microrregiões encontradas.")

        # 3. Transformar os dados JSON em um DataFrame do Pandas
        df = pd.json_normalize(dados_json)

        # 4. Renomear as colunas para um padrão mais limpo
        df.columns = df.columns.str.replace('.', '_', regex=False)
        
        print("\nColunas extraídas e renomeadas:")
        for col in df.columns:
            print(f"  - {col}")

        # 5. Carregar o DataFrame para o banco de dados
        # if_exists='replace' garante que a tabela seja sempre a versão mais atualizada da API.
        print(f"\n📦 Carregando dados para a tabela '{table_name}'...")
        df.to_sql(
            table_name,
            db_engine,
            if_exists='replace',
            index=False
        )
        print(f"✔️ Sucesso! Tabela '{table_name}' criada/atualizada com os dados das microrregiões.")

    except requests.exceptions.RequestException as e:
        print(f"❌ ERRO DE REDE: Falha ao conectar com a API do IBGE. {e}")
    except Exception as e:
        print(f"❌ ERRO CRÍTICO: Ocorreu um problema inesperado. {e}")


# --- CONFIGURAÇÃO PRINCIPAL ---

# 1. Definições do banco de dados (atualizado para o novo nome)
db_file = "DadosBR.db"
db_engine = create_engine(f'sqlite:///{db_file}')

# 2. Nome da nova tabela para armazenar os dados das microrregiões
tabela_microrregioes = "microrregioes"


# --- EXECUÇÃO DO SCRIPT ---

if __name__ == "__main__":
    print("======================================================")
    print("🚀 Iniciando carga de dados das Microrregiões (IBGE)")
    print(f"Banco de dados: {db_file}")
    print("======================================================")
    
    buscar_e_carregar_microrregioes(
        db_engine=db_engine,
        table_name=tabela_microrregioes
    )
    
    print("\n🎉 Processo finalizado.")
