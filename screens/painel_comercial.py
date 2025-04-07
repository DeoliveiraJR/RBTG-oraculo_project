import streamlit as st
from utils import carregar_dados_vendas
import plotly.express as px
import pandas as pd

def exibir():
    st.subheader("📈 Painel Comercial - performance de vendas")

    # Carregar dados
    df = carregar_dados_vendas()

    # Filtros
    col1, col2, col3 = st.columns(3)
    anos = sorted(df['ano'].dropna().unique())
    meses = df['mês'].dropna().unique()
    ufs = df['uf'].dropna().unique()

    with col1:
        ano_sel = st.multiselect("Ano", anos, default=anos)
    with col2:
        mes_sel = st.multiselect("Mês", meses, default=meses)
    with col3:
        uf_sel = st.multiselect("UF", ufs, default=ufs)

    # Aplicar filtros
    df_filtros = df[
        df['ano'].isin(ano_sel) &
        df['mês'].isin(mes_sel) &
        df['uf'].isin(uf_sel)
    ]

    # KPI de faturamento total
    faturamento_total = df_filtros['vr.venda'].sum()
    st.metric("💰 Faturamento Total", f"R$ {faturamento_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    # Gráfico de faturamento ao longo do tempo
    df_mes = df_filtros.groupby(['ano', 'mês'])['vr.venda'].sum().reset_index()
    df_mes['período'] = df_mes['mês'] + " " + df_mes['ano'].astype(str)
    fig = px.line(df_mes, x='período', y='vr.venda', title="Faturamento ao longo do tempo")
    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------------
    # 🎯 Faturamento vs Meta por UF
    # -----------------------------------
    st.markdown("---")
    st.subheader("🎯 Faturamento vs Meta - por UF")

    meta_padrao = 50000
    df_uf = df_filtros.groupby('uf')['vr.venda'].sum().reset_index()
    df_uf['meta'] = meta_padrao
    df_uf['atingido_%'] = (df_uf['vr.venda'] / df_uf['meta']) * 100
    df_uf = df_uf.sort_values(by='vr.venda', ascending=True)

    fig_bar = px.bar(
        df_uf,
        x='vr.venda',
        y='uf',
        orientation='h',
        text='atingido_%',
        color='atingido_%',
        color_continuous_scale='blues',
        labels={'vr.venda': 'Faturamento', 'uf': 'UF', 'atingido_%': '% Atingido'},
        title='Faturamento por UF vs Meta'
    )
    fig_bar.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig_bar.update_layout(xaxis_title='R$ Faturado', yaxis_title='Estado (UF)')
    st.plotly_chart(fig_bar, use_container_width=True)

    # -----------------------------------
    # 🧮 Resultados por mês (melhor/pior)
    # -----------------------------------
    st.markdown("---")
    st.subheader("📊 Resultados ao longo do tempo")

    df_mensal = df_filtros.groupby('mês')['vr.venda'].sum().reset_index()
    melhor = df_mensal.loc[df_mensal['vr.venda'].idxmax()]
    pior = df_mensal.loc[df_mensal['vr.venda'].idxmin()]

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric(f"✅ Melhor mês: {melhor['mês']}", f"R$ {melhor['vr.venda']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    with col_m2:
        st.metric(f"⚠️ Pior mês: {pior['mês']}", f"R$ {pior['vr.venda']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    fig2 = px.line(df_mensal, x='mês', y='vr.venda', title="Variação mensal")
    st.plotly_chart(fig2, use_container_width=True)

    # -----------------------------------
    # 🏆 Ranking de produtos por venda
    # -----------------------------------
    st.markdown("---")
    st.subheader("🏆 Ranking de produtos")

    df_prod = df_filtros.groupby('descricao')['vr.venda'].sum().reset_index()
    df_prod = df_prod.sort_values(by='vr.venda', ascending=False).head(10)
    df_prod['vr.venda'] = df_prod['vr.venda'].map(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    st.table(df_prod.rename(columns={
        'descricao': 'Produto',
        'vr.venda': 'Faturamento'
    }))
