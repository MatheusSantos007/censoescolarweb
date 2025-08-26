import requests
import pandas as pd
from sqlalchemy import create_engine

def buscar_e_carregar_mesorregioes(db_engine, table_name):
    """
    Busca os dados de todas as mesorregiões do Brasil via API do IBGE
    e carrega em uma tabela do banco de dados.
    """
    # URL da API de Mesorregiões do IBGE
    API_URL = "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes?orderBy=nome"
    
    print(f"--- Buscando dados das Mesorregiões na API do IBGE ---")
    print(f"URL: {API_URL}")

    try:
        # 1. Fazer a requisição para a API
        response = requests.get(API_URL)
        response.raise_for_status()  # Lança um erro se a requisição falhar (ex: status 404, 500)
        
        # 2. Converter a resposta JSON em uma lista de dicionários
        dados_json = response.json()
        print(f"✅ {len(dados_json)} mesorregiões encontradas.")

        # 3. Transformar os dados JSON em um DataFrame do Pandas
        # O Pandas é excelente para achatar (flatten) estruturas JSON aninhadas.
        df = pd.json_normalize(dados_json)

        # 4. Renomear as colunas para um padrão mais limpo e amigável
        # Exemplo: 'UF.sigla' se torna 'uf_sigla'
        df.columns = df.columns.str.replace('.', '_', regex=False)
        
        print("\nColunas extraídas e renomeadas:")
        for col in df.columns:
            print(f"  - {col}")

        # 5. Carregar o DataFrame para o banco de dados
        # Usamos if_exists='replace' aqui, pois queremos que a tabela seja
        # sempre a versão mais atualizada da API a cada execução.
        print(f"\n📦 Carregando dados para a tabela '{table_name}'...")
        df.to_sql(
            table_name,
            db_engine,
            if_exists='replace',
            index=False
        )
        print(f"✔️ Sucesso! Tabela '{table_name}' criada/atualizada com os dados das mesorregiões.")

    except requests.exceptions.RequestException as e:
        print(f"❌ ERRO DE REDE: Falha ao conectar com a API do IBGE. {e}")
    except Exception as e:
        print(f"❌ ERRO CRÍTICO: Ocorreu um problema inesperado. {e}")


# --- CONFIGURAÇÃO PRINCIPAL ---

# 1. Definições do banco de dados (o mesmo do script anterior)
db_file = "DadosBR.db"
db_engine = create_engine(f'sqlite:///{db_file}')

# 2. Nome da nova tabela para armazenar os dados das mesorregiões
tabela_mesorregioes = "mesorregioes"


# --- EXECUÇÃO DO SCRIPT ---

if __name__ == "__main__":
    print("======================================================")
    print("🚀 Iniciando carga de dados das Mesorregiões (IBGE)")
    print(f"Banco de dados: {db_file}")
    print("======================================================")
    
    buscar_e_carregar_mesorregioes(
        db_engine=db_engine,
        table_name=tabela_mesorregioes
    )
    
    print("\n🎉 Processo finalizado.")
