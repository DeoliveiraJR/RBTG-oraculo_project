import streamlit as st
from screens import painel_comercial, analise_pareto, mapa_estrategico, oraculo_ia

# ✅ set_page_config deve vir antes de qualquer outro comando streamlit
st.set_page_config(
    layout="wide",
    page_title="Oráculo IA - RBT Medical",
    page_icon="🔮"
)

# Sidebar de navegação
st.sidebar.image("./assets/logo.png", width=200)
st.sidebar.title("🔮 Oráculo")
st.sidebar.markdown("Navegue pelos painéis:")

opcao = st.sidebar.radio("",
    ["Painel Comercial", "Análise de Pareto", "Mapa Estratégico (BSC)", "Oráculo IA"],
    key="menu")

st.sidebar.markdown("---")
st.sidebar.markdown("## 🔍 Filtros")

# Navegação por páginas
if opcao == "Painel Comercial":
    painel_comercial.exibir()
elif opcao == "Análise de Pareto":
    analise_pareto.exibir()
elif opcao == "Mapa Estratégico (BSC)":
    mapa_estrategico.exibir()
elif opcao == "Oráculo IA":
    oraculo_ia.exibir()
