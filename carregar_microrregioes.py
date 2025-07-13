import requests
import pandas as pd
from sqlalchemy import create_engine

def buscar_e_carregar_microrregioes(db_engine, table_name):
   

    API_URL = "https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes?orderBy=nome"
    
    print(f"--- Buscando dados das Microrregiões na API do IBGE ---")
    print(f"URL: {API_URL}")

    try:
        response = requests.get(API_URL)
        response.raise_for_status() 
        dados_json = response.json()
        print(f"✅ {len(dados_json)} microrregiões encontradas.")
        df = pd.json_normalize(dados_json)
        df.columns = df.columns.str.replace('.', '_', regex=False)
        
        print("\nColunas extraídas e renomeadas:")
        for col in df.columns:
            print(f"  - {col}")

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



db_file = "DadosBR.db"
db_engine = create_engine(f'sqlite:///{db_file}')
tabela_microrregioes = "microrregioes"

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
