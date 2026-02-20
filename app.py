import streamlit as st
from supabase import create_client, Client
import os

# 1. Configurações do Supabase (Substitua pelos seus dados do painel do Supabase)
SUPABASE_URL = "https://gpvndtxkdxtezxblpebs.supabase.co"
SUPABASE_KEY = "sb_publishable_m8K253TeQ5lFn1c-DwAf3g_C8ebMcTe"

# Inicializa o cliente Supabase
@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_connection()

# 2. Configuração da Interface
st.set_page_config(page_title="Validador De Críticas", page_icon="✅")

st.title(" Validador")

# 3. Lógica de Validação
with st.form("form_validador"):
    dado_input = st.text_input("Digite o código para validar:", placeholder="Ex: 12345")
    botao_validar = st.form_submit_button("Consultar")

if botao_validar:
    if dado_input:
        try:
            # Busca na sua tabela (ajuste o nome da tabela 'validacoes' se for outro)
            query = supabase.table("criticas").select("*").eq("codigo", dado_input).execute()
            
            if len(query.data) > 0:
                st.success(f"✅ Sucesso! Código '{dado_input}' encontrado.")
                st.json(query.data[0]) # Mostra os detalhes do dado
            else:
                st.error(f"❌ Código '{dado_input}' não encontrado no sistema.")
        except Exception as e:
            st.error(f"Erro de conexão: {e}")
    else:
        st.warning("Por favor, preencha o campo.")

# Rodapé
st.markdown("---")
st.caption("Versão 2.1 - Python Backend")