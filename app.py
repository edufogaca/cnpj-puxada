import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Consulta CNPJ", layout="wide")

# Função para buscar dados
def get_data(url, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None

st.title("⚖️ Sistema de Consulta CNPJ")

# Captura de dados do usuário
cnpj = st.text_input("Digite o CNPJ (apenas números):", placeholder="00000000000000")
days = st.number_input("Defasagem máxima (dias):", min_value=0, value=0)

# O token será puxado de forma segura das configurações
token = st.secrets["API_TOKEN"]

if st.button("Consultar"):
    with st.spinner("Consultando bases de dados..."):
        base_url = "https://receitaws.com.br/v1"
        
        # Chamadas
        dados_cad = get_data(f"{base_url}/cnpj/{cnpj}/days/{days}", token)
        dados_ie = get_data(f"{base_url}/ccc/{cnpj}/days/{days}", token)
        dados_simples = get_data(f"{base_url}/simples/{cnpj}/days/{days}", token)

        # Exibição (Layout em abas para ficar limpo)
        tab1, tab2, tab3 = st.tabs(["Dados Cadastrais", "Inscrição Estadual", "Simples Nacional"])
        
        with tab1:
            st.json(dados_cad)
        with tab2:
            st.json(dados_ie)
        with tab3:
            st.json(dados_simples)