import streamlit as st
import pandas as pd
import plotly.express as px
import openai
from utils import carregar_dados_vendas, gerar_resposta_ia


def exibir():
    df = carregar_dados_vendas()
    st.title("📈 Painel Comercial - performance de vendas")

    # Sidebar com filtros (os títulos já estão no main)
    anos = sorted(df['Ano'].dropna().unique())
    meses = sorted(df['Mês'].dropna().unique(), key=lambda x: pd.to_datetime(x, format='%b').month)
    ufs = sorted(df['UF'].dropna().unique())

    ano_sel = st.sidebar.multiselect("Ano", anos, default=anos)
    mes_sel = st.sidebar.multiselect("Mês", meses, default=meses)
    uf_sel = st.sidebar.multiselect("UF", ufs, default=ufs)

    # Aplicar filtros
    df_filtros = df[
        df['Ano'].isin(ano_sel) &
        df['Mês'].isin(mes_sel) &
        df['UF'].isin(uf_sel)
    ]

    # KPI de faturamento
    st.markdown("### 💵 Faturamento Total")
    faturamento_total = df_filtros['Vr.Venda'].sum()
    st.metric("Total Faturado", f"R$ {faturamento_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    # Gráfico de linha com evolução mensal
    st.markdown("### 📊 Faturamento ao longo do tempo")
    df_mes = df_filtros.groupby(['Ano', 'Mês'])['Vr.Venda'].sum().reset_index()
    df_mes['Período'] = df_mes['Mês'] + " " + df_mes['Ano'].astype(str)

    fig_linha = px.line(
        df_mes,
        x='Período',
        y='Vr.Venda',
        title="Evolução mensal do faturamento",
        markers=True,
        labels={"Vr.Venda": "R$ Faturado"}
    )
    st.plotly_chart(fig_linha, use_container_width=True)

    # 🔍 Análise IA do gráfico acima
    st.markdown("### 🤖 Insight da IA")
    contexto = f"Dados de faturamento mensal: {df_mes.to_dict(orient='records')}"
    insight = gerar_resposta_ia(contexto)
    st.markdown(insight)

    pergunta = st.text_input("💬 Faça uma pergunta sobre os dados")
    if pergunta:
        resposta = gerar_resposta_ia(contexto + f"\nPergunta: {pergunta}")
        st.markdown(resposta)

    # Tabela de ranking de produtos
    st.markdown("### 🏆 Ranking de Produtos")
    ranking = df_filtros.groupby('Produto')['Vr.Venda'].sum().sort_values(ascending=False).head(10).reset_index()
    ranking.columns = ['Produto', 'Faturamento']
    ranking['Faturamento'] = ranking['Faturamento'].map(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    st.table(ranking)
