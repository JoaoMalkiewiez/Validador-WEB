from flask import Flask, render_template, request, jsonify
import os
from supabase import create_client, Client

app = Flask(__name__, static_folder='static', template_folder='templates')

# Credenciais Diretas para evitar falhas de ambiente
SUPABASE_URL = "https://gpvndtxkdxtezxblpebs.supabase.co"
SUPABASE_KEY = "sb_publishable_m8K253TeQ5lFn1c-DwAf3g_C8ebMcTe"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    # Isso garante que sua página real carregue, não a tela de teste genérica
    return render_template('index.html')

@app.route('/criticas')
def listar_criticas():
    termo = request.args.get('busca', '')
    try:
        # Busca na coluna correta conforme o seu commit
        if termo:
            query = supabase.table("criticas").select("*").ilike("critica", f"%{termo}%").execute()
        else:
            query = supabase.table("criticas").select("*").execute()
        
        return render_template('criticas.html', dados=query.data if query.data else [], busca=termo)
    except Exception as e:
        print(f"Erro no banco: {e}")
        return f"Erro de conexão: {e}"

if __name__ == '__main__':
    # Porta dinâmica para o Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)