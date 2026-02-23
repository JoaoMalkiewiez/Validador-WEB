from flask import Flask, render_template, request
import os
from supabase import create_client

app = Flask(__name__)

# Credenciais do Supabase
URL = "https://gpvndtxkdxtezxblpebs.supabase.co"
KEY = "sb_publishable_m8K253TeQ5lFn1c-DwAf3g_C8ebMcTe"
supabase = create_client(URL, KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/criticas')
def listar_criticas():
    termo = request.args.get('busca', '')
    try:
        # Busca na coluna 'critica' conforme seu banco real
        if termo:
            query = supabase.table("criticas").select("*").ilike("critica", f"%{termo}%").execute()
        else:
            query = supabase.table("criticas").select("*").execute()
        return render_template('criticas.html', dados=query.data, busca=termo)
    except Exception as e:
        return f"Erro: {e}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)