from flask import Flask, render_template, request
import os
from supabase import create_client

# Configura explicitamente as pastas para o Render
app = Flask(__name__, template_folder='templates')

# Credenciais do Supabase
URL = "https://gpvndtxkdxtezxblpebs.supabase.co"
KEY = "sb_publishable_m8K253TeQ5lFn1c-DwAf3g_C8ebMcTe"
supabase = create_client(URL, KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/criticas')
def listar_criticas():
    termo = request.args.get('busca', '').strip()
    try:
        if termo:
            # Busca em todas as colunas reais identificadas
            filtro = f"critica.ilike.%{termo}%,motivo.ilike.%{termo}%,como_resolver.ilike.%{termo}%,encaminhar_para.ilike.%{termo}%"
            query = supabase.table("criticas").select("*").or_(filtro).execute()
        else:
            query = supabase.table("criticas").select("*").execute()
        
        # Se chegar aqui, o carregamento funcionou
        return render_template('criticas.html', dados=query.data, busca=termo)
    
    except Exception as e:
        # Se travar, ele mostrará o erro técnico na tela em vez de ficar carregando infinito
        return f"<h3>Erro de Carregamento</h3><p>Detalhes: {str(e)}</p><a href='/'>Voltar</a>", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)