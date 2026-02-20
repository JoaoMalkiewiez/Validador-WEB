from flask import Flask, render_template, request, jsonify, send_file
import tempfile, os, io, uuid, shutil
import xml.etree.ElementTree as ET
from supabase import create_client, Client

# Importa a lógica do arquivo validador_fiscal.py que deve estar na mesma pasta
try:
    from validador_fiscal import ValidadorFiscal
except ImportError:
    class ValidadorFiscal:
        def build_events_index(self, p): return {}
        def extrair_dados_xml(self, p, t, events_index=None): return {}
        def limpar_tag(self, tag): return tag.split('}')[-1]

app = Flask(__name__, static_folder='static', template_folder='templates')

# Armazenamento temporário para resultados processados
STORE = {}

# Credenciais do Supabase (Extraídas do seu ambiente atual)
SUPABASE_URL = "https://gpvndtxkdxtezxblpebs.supabase.co"
SUPABASE_KEY = "sb_publishable_m8K253TeQ5lFn1c-DwAf3g_C8ebMcTe"

# Conexão Flask Pura (Compatível com Gunicorn e Render)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    # Retorna o seu template principal do validador
    return render_template('index.html')

@app.route('/criticas')
def listar_criticas():
    termo = request.args.get('busca', '')
    try:
        # Realiza a busca na coluna 'critica' conforme seu banco real
        if termo:
            query = supabase.table("criticas").select("*").ilike("critica", f"%{termo}%").execute()
        else:
            query = supabase.table("criticas").select("*").execute()
        
        # Renderiza os dados nos cards (templates/criticas.html)
        return render_template('criticas.html', dados=query.data if query.data else [], busca=termo)
    except Exception as e:
        print(f"Erro Supabase: {e}")
        return f"Erro ao acessar o banco de dados: {e}"

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
                tree = ET.parse(p)
                root = tree.getroot()
                is_nota = any(validator.limpar_tag(el.tag).lower() == 'infnfe' for el in root.iter())
                if is_nota:
                    dados = validator.extrair_dados_xml(p, tipo, events_index=events_index)
                    if dados.get('Número') and dados.get('Número') != '0.00':
                        notas.append(dados)
            except:
                continue

        key = str(uuid.uuid4())
        STORE[key] = notas
        shutil.rmtree(tmpdir)

        return jsonify({'id': key, 'count': len(notas), 'notas': notas})
    except Exception as e:
        return jsonify({'error': 'Erro interno', 'detail': str(e)}), 500

@app.route('/download/<key>')
def download(key):
    notas = STORE.get(key)
    if not notas:
        return 'ID não encontrado', 404
    
    import xlsxwriter
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Notas')
    # Cabeçalhos básicos
    headers = ['Tipo', 'Data', 'Número', 'Status', 'Total']
    for col, h in enumerate(headers):
        worksheet.write(0, col, h)
    
    # Preenchimento simples das notas
    for row, nota in enumerate(notas, start=1):
        worksheet.write(row, 0, nota.get('Tipo', ''))
        worksheet.write(row, 1, nota.get('Data', ''))
        worksheet.write(row, 2, nota.get('Número', ''))
        worksheet.write(row, 3, nota.get('Status', ''))
        worksheet.write(row, 4, nota.get('Total', 0.0))
        
    workbook.close()
    output.seek(0)
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='notas.xlsx')

if __name__ == '__main__':
    # Porta padrão para desenvolvimento local
    app.run(debug=True, host='0.0.0.0', port=5000)