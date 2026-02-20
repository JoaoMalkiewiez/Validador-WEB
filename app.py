import streamlit as st
from supabase import create_client, Client

# Configurações do Supabase
SUPABASE_URL = "https://gpvndtxkdxtezxblpebs.supabase.co"
SUPABASE_KEY = "sb_publishable_m8K253TeQ5lFn1c-DwAf3g_C8ebMcTe"

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_connection()

# Estilização para ficar igual ao App
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #007bff; color: white; width: 100%; border-radius: 5px; }
    .critica-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    .titulo-erro { color: #d9534f; font-weight: bold; font-size: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("🔎 Consultar Críticas de Suporte")

# Campo de busca idêntico ao App
with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
        busca = st.text_input("", placeholder="Digite o erro (ex: consumo)", label_visibility="collapsed")
    with col2:
        botao = st.button("BUSCAR")

if botao and busca:
    try:
        # BUSCA: Ajustei para procurar na coluna 'motivo' conforme sugerido pelo erro
        # Se sua coluna de busca for 'critica', mude .eq("motivo", busca) para .eq("critica", busca)
        query = supabase.table("criticas").select("*").ilike("motivo", f"%{busca}%").execute()
        
        if query.data:
            item = query.data[0]
            # Layout de retorno igual ao App
            st.markdown(f"""
                <div class="critica-card">
                    <div class="titulo-erro">🚩 {item.get('motivo', 'Erro')}</div>
                    <p>💡 <b>Motivo:</b> {item.get('causa', 'Não informado')}</p>
                    <p>🛠️ <b>Como Resolver:</b> {item.get('resolucao', 'Não informado')}</p>
                    <p>⏩ <b>Encaminhar para:</b> {item.get('setor', 'Suporte N1')}</p>
                    <small>🔥 Utilizado recentemente pela equipe</small>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Nenhuma crítica encontrada para este termo.")
    except Exception as e:
        st.error(f"Erro ao consultar banco: {e}")

st.markdown("---")
st.caption("Versão 2.1 - Sincronizado com Banco de Dados")