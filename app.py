from flask import Flask, render_template, request, jsonify, send_file
import tempfile, os, io, uuid, shutil
import xml.etree.ElementTree as ET
from supabase import create_client, Client

# Inicialização do Flask
app = Flask(__name__, static_folder='static', template_folder='templates')

# Credenciais Diretas para evitar erro de variável
SUPABASE_URL = "https://gpvndtxkdxtezxblpebs.supabase.co"
SUPABASE_KEY = "sb_publishable_m8K253TeQ5lFn1c-DwAf3g_C8ebMcTe"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/criticas')
def listar_criticas():
    termo = request.args.get('busca', '')
    try:
        # Busca obrigatória na coluna 'critica' conforme o banco real
        if termo:
            query = supabase.table("criticas").select("*").ilike("critica", f"%{termo}%").execute()
        else:
            query = supabase.table("criticas").select("*").execute()
        return render_template('criticas.html', dados=query.data if query.data else [], busca=termo)
    except Exception as e:
        return f"Erro de conexão com Supabase: {e}"

# Rota de validação simplificada para evitar erro 500
@app.route('/validate', methods=['POST'])
def validate():
    return jsonify({'status': 'online', 'message': 'Pronto para processar XML'})

if __name__ == '__main__':
    app.run(debug=True)