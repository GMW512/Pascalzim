from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess, uuid, os

app = Flask(__name__)
CORS(app)

@app.route('/executar', methods=['POST'])
def executar():
    codigo = request.json.get('codigo')
    nome_arquivo = f"/tmp/{uuid.uuid4()}.pas"

    with open(nome_arquivo, 'w') as f:
        f.write(codigo)

    try:
        resultado = subprocess.run(
            ["pascalzim", nome_arquivo],
            capture_output=True,
            text=True,
            timeout=5
        )
        return jsonify({
            'saida': resultado.stdout,
            'erros': resultado.stderr
        })
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        os.remove(nome_arquivo)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
