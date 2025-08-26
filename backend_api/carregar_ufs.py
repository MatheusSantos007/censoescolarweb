import requests
import pandas as pd
from sqlalchemy import create_engine

def buscar_e_carregar_ufs(db_engine, table_name):
    """
    Busca os dados de todas as Unidades da Federação (UFs) do Brasil 
    via API do IBGE e carrega em uma tabela do banco de dados.
    """
    # URL da API de UFs (Estados) do IBGE
    API_URL = "https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome"
    
    print(f"--- Buscando dados das UFs na API do IBGE ---")
    print(f"URL: {API_URL}")

    try:
        # 1. Fazer a requisição para a API
        response = requests.get(API_URL)
        response.raise_for_status()
        
        dados_json = response.json()
        print(f"✅ {len(dados_json)} UFs encontradas.")

        # 2. Transformar os dados JSON em um DataFrame do Pandas
        df_bruto = pd.json_normalize(dados_json)

        # 3. Definir o mapeamento das colunas para manter a tabela limpa
        mapa_colunas = {
            'id': 'id',
            'sigla': 'sigla',
            'nome': 'nome',
            'regiao.id': 'regiao_id',
            'regiao.sigla': 'regiao_sigla',
            'regiao.nome': 'regiao_nome'
        }
        
        # 4. Selecionar e renomear as colunas
        df_selecionado = df_bruto[list(mapa_colunas.keys())]
        df_final = df_selecionado.rename(columns=mapa_colunas)

        print("\nColunas selecionadas e renomeadas para o padrão final:")
        for col in df_final.columns:
            print(f"  - {col}")

        # 5. Carregar o DataFrame para o banco de dados
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


# --- CONFIGURAÇÃO PRINCIPAL ---

# 1. Definições do banco de dados
db_file = "DadosBR.db"
db_engine = create_engine(f'sqlite:///{db_file}')

# 2. Nome da nova tabela para armazenar os dados das UFs
tabela_ufs = "ufs"


# --- EXECUÇÃO DO SCRIPT ---

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
