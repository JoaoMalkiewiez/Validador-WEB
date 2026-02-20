import streamlit as st
from supabase import create_client, Client

# Configurações do Supabase
SUPABASE_URL = "https://gpvndtxkdxtezxblpebs.supabase.co"
SUPABASE_KEY = "sb_publishable_m8K253TeQ5lFn1c-DwAf3g_C8ebMcTe"

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_connection()

# Estilização idêntica ao App de Suporte
st.markdown("""
    <style>
    .stApp { background-color: #0f1116; color: white; }
    .stButton>button { background-color: #007bff; color: white; width: 100%; border: none; height: 45px; }
    .critica-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        color: #333;
        margin-top: 20px;
    }
    .titulo-erro { color: #d9534f; font-weight: bold; font-size: 18px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🔍 Consultar Críticas de Suporte")

# Interface de busca
with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
        busca = st.text_input("", placeholder="Digite a crítica ou erro...", label_visibility="collapsed")
    with col2:
        botao = st.button("BUSCAR")

if (botao or busca) and busca:
    try:
        # BUSCA CORRIGIDA: Agora busca na coluna 'critica' que existe no seu banco
        # O .ilike permite busca parcial (ex: digitar apenas 'desconto')
        query = supabase.table("criticas").select("*").ilike("critica", f"%{busca}%").execute()
        
        if query.data:
            for item in query.data:
                # Mapeamento exato das colunas da sua imagem
                st.markdown(f"""
                    <div class="critica-card">
                        <div class="titulo-erro">🚩 {item.get('critica', 'Erro')}</div>
                        <p>💡 <b>Motivo:</b> {item.get('motivo', 'Não informado')}</p>
                        <p>🛠️ <b>Como Resolver:</b> {item.get('como_resolver', 'Consulte o N2')}</p>
                        <p>⏩ <b>Encaminhar para:</b> Suporte N1</p>
                        <small>🔥 Utilizado recentemente pela equipe</small>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning(f"Nenhuma crítica encontrada para: {busca}")
    except Exception as e:
        st.error(f"Erro na consulta: {e}")

st.markdown("---")
st.caption("Validador")