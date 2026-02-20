from flask import Flask, render_template, request, jsonify, send_file
import tempfile, os, io, uuid, shutil
import xml.etree.ElementTree as ET
from supabase import create_client, Client

# Importa a lógica do seu arquivo validador_fiscal.py
try:
    from validador_fiscal import ValidadorFiscal
except ImportError:
    class ValidadorFiscal:
        def build_events_index(self, p): return {}
        def extrair_dados_xml(self, p, t, events_index=None): return {}

app = Flask(__name__, static_folder='static', template_folder='templates')

STORE = {}

# Credenciais do Supabase
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
        # Busca na coluna 'critica' do seu banco de dados
        if termo:
            query = supabase.table("criticas").select("*").ilike("critica", f"%{termo}%").execute()
        else:
            query = supabase.table("criticas").select("*").execute()
        return render_template('criticas.html', dados=query.data if query.data else [], busca=termo)
    except Exception as e:
        return f"Erro de conexão: {e}"

@app.route('/validate', methods=['POST'])
def validate():
    try:
        tipo = request.form.get('tipo', 'NF-e')
        files = request.files.getlist('files')
        if not files:
            return jsonify({'error':'Nenhum arquivo enviado'}), 400

        tmpdir = tempfile.mkdtemp(prefix='val_')
        paths = []
        for f in files:
            filename = os.path.basename(f.filename) or str(uuid.uuid4()) + '.xml'
            dest = os.path.join(tmpdir, filename)
            f.save(dest)
            paths.append(dest)

        validator = ValidadorFiscal()
        events_index = validator.build_events_index(paths)
        
        notas = []
        for p in paths:
            try:
                dados = validator.extrair_dados_xml(p, tipo, events_index=events_index)
                if dados.get('Número'):
                    notas.append(dados)
            except:
                continue

        key = str(uuid.uuid4())
        STORE[key] = notas
        shutil.rmtree(tmpdir)
        return jsonify({'id': key, 'count': len(notas), 'notas': notas})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)