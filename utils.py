import pandas as pd

def carregar_dados_vendas(caminho='./dataset/Tabela Fato/fVendas.csv'):
    df = pd.read_csv(caminho, sep=';', encoding='latin1')

    # Padronizar nomes de colunas
    df.columns = df.columns.str.strip().str.lower()

    # Conversões e limpeza
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y', errors='coerce')
    df['ano'] = df['data'].dt.year
    df['mês'] = df['data'].dt.month_name().str[:3]
    df['uf'] = df['uf'].fillna('Não informado')
    df['vr.venda'] = pd.to_numeric(df['vr.venda'], errors='coerce').fillna(0)

    return df
