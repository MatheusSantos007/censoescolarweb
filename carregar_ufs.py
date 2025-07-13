import requests
import pandas as pd
from sqlalchemy import create_engine

def buscar_e_carregar_ufs(db_engine, table_name):

    API_URL = "https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome"
    
    print(f"--- Buscando dados das UFs na API do IBGE ---")
    print(f"URL: {API_URL}")

    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        
        dados_json = response.json()
        print(f"✅ {len(dados_json)} UFs encontradas.")
        df_bruto = pd.json_normalize(dados_json)
        mapa_colunas = {
            'id': 'id',
            'sigla': 'sigla',
            'nome': 'nome',
            'regiao.id': 'regiao_id',
            'regiao.sigla': 'regiao_sigla',
            'regiao.nome': 'regiao_nome'
        }
        df_selecionado = df_bruto[list(mapa_colunas.keys())]
        df_final = df_selecionado.rename(columns=mapa_colunas)

        print("\nColunas selecionadas e renomeadas para o padrão final:")
        for col in df_final.columns:
            print(f"  - {col}")

        print(f"\n📦 Carregando dados para a tabela '{table_name}'...")
        df_final.to_sql(
            table_name,
            db_engine,
            if_exists='replace',
            index=False
        )
        print(f"✔️ Sucesso! Tabela '{table_name}' criada/atualizada com os dados das UFs.")

    except requests.exceptions.RequestException as e:
        print(f"❌ ERRO DE REDE: Falha ao conectar com a API do IBGE. {e}")
    except Exception as e:
        print(f"❌ ERRO CRÍTICO: Ocorreu um problema inesperado. {e}")


db_file = "DadosBR.db"
db_engine = create_engine(f'sqlite:///{db_file}')
tabela_ufs = "ufs"


if __name__ == "__main__":
    print("======================================================")
    print("🚀 Iniciando carga de dados das UFs (IBGE)")
    print(f"Banco de dados: {db_file}")
    print("======================================================")
    
    buscar_e_carregar_ufs(
        db_engine=db_engine,
        table_name=tabela_ufs
    )
    
    print("\n🎉 Processo finalizado.")
