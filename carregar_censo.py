import pandas as pd
from sqlalchemy import create_engine
import re
import os

def processar_e_carregar_csv(file_path, db_engine, table_name, colunas):

    print(f"\n--- Processando arquivo: {file_path} ---")

    if not os.path.exists(file_path):
        print(f"❌ ERRO: Arquivo não encontrado. Pulando: {file_path}")
        return

    match = re.search(r'_(\d{4})\.csv', file_path)
    if not match:
        print(f"⚠️ AVISO: Não foi possível determinar o ano pelo nome do arquivo. Pulando: {file_path}")
        return
    
    ano_censo = int(match.group(1))
    print(f"🔎 Ano identificado: {ano_censo}")

    try:

        print("🔄 Lendo arquivo CSV (isso pode levar alguns minutos)...")
        df = pd.read_csv(
            file_path,
            sep=';',
            encoding='latin1',
            usecols=colunas,
            low_memory=False
        )

        df['ano'] = ano_censo
        print(f"✅ Coluna 'ano' com o valor '{ano_censo}' adicionada.")

        print(f"📦 Carregando {len(df):,} registros para a tabela '{table_name}'...")
        df.to_sql(
            table_name,
            db_engine,
            if_exists='append',
            index=False, 
            chunksize=10000 
        )
        print(f"✔️ Sucesso! Dados de {file_path} carregados.")

    except Exception as e:
        print(f"❌ ERRO CRÍTICO ao processar {file_path}: {e}")
        print("   Verifique se os nomes em 'colunas_selecionadas' existem no arquivo CSV.")



arquivos_censo = [
    'microdados_ed_basica_2023.csv',
    'microdados_ed_basica_2024.csv'
]

db_file = "DadosBR.db"
tabela = "instituicoes"
db_engine = create_engine(f'sqlite:///{db_file}')

colunas_selecionadas = [
    "NO_REGIAO", "CO_REGIAO", "NO_UF", "SG_UF", "CO_UF", "NO_MUNICIPIO", 
    "CO_MUNICIPIO", "NO_MESORREGIAO", "NO_MICRORREGIAO", "NO_ENTIDADE", 
    "CO_ENTIDADE", "QT_MAT_BAS", "QT_MAT_INF", "QT_MAT_FUND", "QT_MAT_MED", 
    "QT_MAT_EJA", "QT_MAT_EJA_FUND", "QT_MAT_ESP", "QT_MAT_BAS_EAD", 
    "QT_MAT_FUND_INT", "QT_MAT_MED_INT"
]


if __name__ == "__main__":
    print("======================================================")
    print("🚀 Iniciando carga de dados do Censo Escolar para SQLite")
    print(f"Banco de dados: {db_file}")
    print(f"Tabela: {tabela}")
    print("======================================================")

    for csv_file in arquivos_censo:
        processar_e_carregar_csv(
            file_path=csv_file,
            db_engine=db_engine,
            table_name=tabela, 
            colunas=colunas_selecionadas
        )
    
    print("\n🎉 Processo de carga de dados finalizado com sucesso!")
