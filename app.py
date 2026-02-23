from flask import Flask, render_template, request
import os
from supabase import create_client

# Configuração para garantir que o Flask encontre os templates
app = Flask(__name__, template_folder='templates')

# Credenciais do Supabase
URL = "https://gpvndtxkdxtezxblpebs.supabase.co"
KEY = "sb_publishable_m8K253TeQ5lFn1c-DwAf3g_C8ebMcTe"
supabase = create_client(URL, KEY)

@app.route('/')
def index():
    # Renderiza a página principal de busca
    return render_template('index.html')

@app.route('/criticas')
def listar_criticas():
    termo = request.args.get('busca', '')
    try:
        # Busca no Supabase usando ilike para não diferenciar maiúsculas/minúsculas
        if termo:
            query = supabase.table("criticas").select("*").ilike("critica", f"%{termo}%").execute()
        else:
            query = supabase.table("criticas").select("*").execute()
        
        # Retorna a página de resultados com os dados do banco
        return render_template('criticas.html', dados=query.data, busca=termo)
    except Exception as e:
        # Em produção, o Render mostrará esse erro se a conexão falhar
        return f"Erro na conexão com o banco de dados: {e}"

if __name__ == '__main__':
    # Configuração de porta dinâmica para o Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)