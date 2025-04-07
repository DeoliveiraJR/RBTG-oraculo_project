import streamlit as st
from screens import painel_comercial, analise_pareto, mapa_estrategico, oraculo_ia

# Configurações da página
st.set_page_config(
    page_title="Oráculo-RBTG",
    layout="wide",
    page_icon="📊"
)

# Sidebar - Navegação
st.sidebar.image("./assets/logo.png", width=150)
st.sidebar.title("🔮 Oráculo")
pagina = st.sidebar.radio(
    "Navegue pelos painéis:",
    [
        "Painel Comercial",
        "Análise de Pareto",
        "Mapa Estratégico (BSC)",
        "Oráculo IA"
    ]
)

# Conteúdo da Página
st.title("🔍 Dashboard Executivo Oráculo")

if pagina == "Painel Comercial":
    painel_comercial.exibir()
elif pagina == "Análise de Pareto":
    analise_pareto.exibir()
elif pagina == "Mapa Estratégico (BSC)":
    mapa_estrategico.exibir()
elif pagina == "Oráculo IA":
    oraculo_ia.exibir()
