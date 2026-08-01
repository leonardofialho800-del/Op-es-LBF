import os
from flask import Flask, request, jsonify
import google.generativeai as genai

# Pega a chave de forma segura direto do servidor (Render)
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Escolhendo o modelo de IA que vai gerar os textos
modelo_ia = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Robo com IA Ativada e Pronto para Trabalhar!"

# A ROTA MÁGICA: Onde a IA gera os textos
@app.route('/gerar-copy', methods=['POST'])
def gerar_copy():
    dados = request.json
    tema = dados.get('tema', 'Sem tema')
    
    instrucao_para_ia = f"Escreva uma legenda persuasiva e profissional para o Instagram sobre o seguinte tema: {tema}. Inclua 5 hashtags."
    resposta_da_ia = modelo_ia.generate_content(instrucao_para_ia)
    
    return jsonify({
        "status": "sucesso", 
        "tema_pedido": tema,
        "copy_gerada": resposta_da_ia.text
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

