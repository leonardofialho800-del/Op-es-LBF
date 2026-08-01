from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Robo Rodando na Nuvem com Sucesso!"

@app.route('/gerar-copy', methods=['POST'])
def gerar_copy():
    dados = request.json
    tema = dados.get('tema', 'Sem tema')
    return jsonify({"status": "sucesso", "mensagem": f"Copy sobre {tema} gerada!"})

if __name__ == '__main__':
    # O Render precisa que a porta e o host sejam definidos assim
    app.run(host='0.0.0.0', port=10000)
