import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
import google.generativeai as genai

# Carregar .env
load_dotenv()
GEMINI_API_KEY="AIzaSyCp5qA9-gGJKS128TeBpYl85Zclrxz5vNc"


# Inicializar cliente da OpenAI (nova interface)
# client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"))

# Configure a chave de API
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
genai.configure(api_key={GEMINI_API_KEY})
print(os.getenv("GEMINI_API_KEY"))

# Caminho do dataset
CAMINHO_ARQUIVO = "./dataset/Tabela Fato/fVendas.csv"


def carregar_dados_vendas():
    df = pd.read_csv(CAMINHO_ARQUIVO, sep=";")

    if 'Data' in df.columns:
        df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
        df['Ano'] = df['Data'].dt.year
        df['Mês'] = df['Data'].dt.strftime('%b')

    if 'Vr.Venda' in df.columns:
        df['Vr.Venda'] = pd.to_numeric(df['Vr.Venda'], errors='coerce').fillna(0)

    return df


# def gerar_resposta_ia(contexto, modelo="gpt-3.5-turbo", temperatura=0.4):
#     prompt = f"""
#     Você é um analista de BI. Analise os dados a seguir e gere insights claros e objetivos, como se estivesse explicando para um gestor comercial.
    
#     Dados: {contexto}
#     """

#     try:
#         resposta = client.chat.completions.create(
#             model=modelo,
#             messages=[
#                 {"role": "system", "content": "Você é um analista de BI que ajuda com insights de dashboards."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=temperatura,
#             max_tokens=600
#         )
#         return resposta.choices[0].message.content
#     except Exception as e:
#         return f"⚠️ Erro ao gerar análise da IA: {str(e)}"


# Função de geração de insights com IA do Gemini
def gerar_resposta_ia(contexto, modelo="gemini-1.5-pro-latest", temperatura=0.4):
    prompt = f"""
    Você é um analista de BI. Analise os dados a seguir e gere insights claros e objetivos, como se estivesse explicando para um gestor comercial.
    
    Dados: {contexto}
    """

    try:
        model = genai.GenerativeModel(modelo)
        resposta = model.generate_content(prompt, generation_config={"temperature": temperatura})
        return resposta.text
    except Exception as e:
        return f"⚠️ Erro ao gerar análise da IA: {str(e)}"
