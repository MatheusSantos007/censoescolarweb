import pandas as pd
from sqlalchemy import create_engine
import re
import os

def processar_e_carregar_csv(file_path, db_engine, table_name, colunas):
    """
    Processa um único arquivo CSV do Censo e o carrega em uma tabela do banco de dados.

    Esta função substitui a leitura linha a linha por uma carga em massa com Pandas,
    o que é significativamente mais rápido para arquivos grandes.
    """
    print(f"\n--- Processando arquivo: {file_path} ---")

    # 1. Validação: Verifica se o arquivo realmente existe
    if not os.path.exists(file_path):
        print(f"❌ ERRO: Arquivo não encontrado. Pulando: {file_path}")
        return

    # 2. Extrai o ano do nome do arquivo (ex: '2023' de 'microdados_ed_basica_2023.csv')
    # Esta é a etapa chave para diferenciar os dados de cada ano.
    match = re.search(r'_(\d{4})\.csv', file_path)
    if not match:
        print(f"⚠️ AVISO: Não foi possível determinar o ano pelo nome do arquivo. Pulando: {file_path}")
        return
    
    ano_censo = int(match.group(1))
    print(f"🔎 Ano identificado: {ano_censo}")

    try:
        # 3. Leitura do CSV com Pandas
        # Usar 'usecols' carrega apenas as colunas necessárias, economizando muita memória.
        # Os arquivos do INEP geralmente usam separador ';' e codificação 'latin1'.
        print("🔄 Lendo arquivo CSV (isso pode levar alguns minutos)...")
        df = pd.read_csv(
            file_path,
            sep=';',
            encoding='latin1',
            usecols=colunas,
            low_memory=False
        )

        # 4. Adiciona a coluna 'ano' ao DataFrame
        # Agora cada registro terá a informação do seu respectivo ano do censo.
        df['ano'] = ano_censo
        print(f"✅ Coluna 'ano' com o valor '{ano_censo}' adicionada.")

        # 5. Carrega os dados para o banco de dados
        # O 'if_exists='append'' garante que os dados de 2024 sejam adicionados
        # após os de 2023, sem apagar a tabela.
        print(f"📦 Carregando {len(df):,} registros para a tabela '{table_name}'...")
        df.to_sql(
            table_name,
            db_engine,
            if_exists='append',
            index=False, # Não salva o índice do DataFrame como uma coluna no DB
            chunksize=10000 # Insere os dados em lotes para otimizar o uso de memória
        )
        print(f"✔️ Sucesso! Dados de {file_path} carregados.")

    except Exception as e:
        print(f"❌ ERRO CRÍTICO ao processar {file_path}: {e}")
        print("   Verifique se os nomes em 'colunas_selecionadas' existem no arquivo CSV.")


# --- CONFIGURAÇÃO PRINCIPAL ---

# 1. Lista de arquivos a serem processados.
#    O script irá iterar sobre esta lista.
arquivos_censo = [
    'microdados_ed_basica_2023.csv',
    'microdados_ed_basica_2024.csv'
]

# 2. Definições do banco de dados.
#    Usando um nome de arquivo sem vírgulas para evitar problemas.
db_file = "DadosBR.db"
tabela = "instituicoes"
db_engine = create_engine(f'sqlite:///{db_file}')

# 3. Colunas que você deseja extrair do CSV.
colunas_selecionadas = [
    "NO_REGIAO", "CO_REGIAO", "NO_UF", "SG_UF", "CO_UF", "NO_MUNICIPIO", 
    "CO_MUNICIPIO", "NO_MESORREGIAO", "NO_MICRORREGIAO", "NO_ENTIDADE", 
    "CO_ENTIDADE", "QT_MAT_BAS", "QT_MAT_INF", "QT_MAT_FUND", "QT_MAT_MED", 
    "QT_MAT_EJA", "QT_MAT_EJA_FUND", "QT_MAT_ESP", "QT_MAT_BAS_EAD", 
    "QT_MAT_FUND_INT", "QT_MAT_MED_INT"
]


# --- EXECUÇÃO DO SCRIPT ---

if __name__ == "__main__":
    print("======================================================")
    print("🚀 Iniciando carga de dados do Censo Escolar para SQLite")
    print(f"Banco de dados: {db_file}")
    print(f"Tabela: {tabela}")
    print("======================================================")

    # Loop principal que processa cada arquivo da lista
    for csv_file in arquivos_censo:
        processar_e_carregar_csv(
            file_path=csv_file,
            db_engine=db_engine,
            table_name=tabela, # <-- CORREÇÃO APLICADA AQUI
            colunas=colunas_selecionadas
        )
    
    print("\n🎉 Processo de carga de dados finalizado com sucesso!")
