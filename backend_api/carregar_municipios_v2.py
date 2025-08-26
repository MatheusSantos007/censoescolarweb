import requests
import pandas as pd
from sqlalchemy import create_engine

def buscar_e_carregar_municipios_v2(db_engine, table_name):
    """
    Busca os dados de todos os municípios do Brasil, seleciona e renomeia
    colunas específicas e carrega em uma tabela do banco de dados.
    """
    # URL da API de Municípios do IBGE
    API_URL = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios?orderBy=nome"
    
    print(f"--- Buscando dados dos Municípios na API do IBGE ---")
    print(f"URL: {API_URL}")
    print("Aguarde, esta operação pode levar alguns instantes...")

    try:
        # 1. Fazer a requisição para a API
        response = requests.get(API_URL)
        response.raise_for_status()
        
        dados_json = response.json()
        print(f"✅ {len(dados_json)} municípios encontrados.")

        # 2. Transformar os dados JSON em um DataFrame do Pandas
        df_bruto = pd.json_normalize(dados_json)

        # 3. Definir o mapeamento das colunas originais para os novos nomes desejados
        mapa_colunas = {
            'id': 'id',
            'nome': 'nome',
            'microrregiao.id': 'microrregiao_id',
            'microrregiao.nome': 'microrregiao_nome',
            'microrregiao.mesorregiao.id': 'mesorregiao_id',
            'microrregiao.mesorregiao.nome': 'mesorregiao_nome',
            'microrregiao.mesorregiao.UF.id': 'uf_id',
            'microrregiao.mesorregiao.UF.sigla': 'uf_sigla',
            'microrregiao.mesorregiao.UF.nome': 'uf_nome',
            'microrregiao.mesorregiao.UF.regiao.id': 'regiao_id',
            'microrregiao.mesorregiao.UF.regiao.sigla': 'regiao_sigla',
            'microrregiao.mesorregiao.UF.regiao.nome': 'regiao_nome'
        }
        
        # 4. Selecionar apenas as colunas que vamos usar
        df_selecionado = df_bruto[list(mapa_colunas.keys())]
        
        # 5. Renomear as colunas selecionadas para o padrão final
        df_final = df_selecionado.rename(columns=mapa_colunas)

        print("\nColunas selecionadas e renomeadas para o padrão final:")
        for col in df_final.columns:
            print(f"  - {col}")

        # 6. Carregar o DataFrame final e limpo para o banco de dados
        print(f"\n📦 Carregando dados para a tabela '{table_name}'...")
        df_final.to_sql(
            table_name,
            db_engine,
            if_exists='replace',
            index=False
        )
        print(f"✔️ Sucesso! Tabela '{table_name}' criada/atualizada com os dados dos municípios.")

    except requests.exceptions.RequestException as e:
        print(f"❌ ERRO DE REDE: Falha ao conectar com a API do IBGE. {e}")
    except Exception as e:
        print(f"❌ ERRO CRÍTICO: Ocorreu um problema inesperado. {e}")


# --- CONFIGURAÇÃO PRINCIPAL ---

# 1. Definições do banco de dados
db_file = "DadosBR.db"
db_engine = create_engine(f'sqlite:///{db_file}')

# 2. Nome da nova tabela para armazenar os dados dos municípios
tabela_municipios = "municipios"


# --- EXECUÇÃO DO SCRIPT ---

if __name__ == "__main__":
    print("======================================================")
    print("🚀 Iniciando carga de dados dos Municípios (v2 - Colunas Selecionadas)")
    print(f"Banco de dados: {db_file}")
    print("======================================================")
    
    buscar_e_carregar_municipios_v2(
        db_engine=db_engine,
        table_name=tabela_municipios
    )
    
    print("\n🎉 Processo finalizado.")
