import os
from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai

api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

modelo_ia = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)

# Página visual mobile moderna e limpa
HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Robô de Copywriting - LBF</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; color: #333; }
        .container { max-width: 500px; margin: 20px auto; background: #fff; padding: 24px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        h2 { text-align: center; color: #1a73e8; margin-bottom: 20px; }
        label { font-weight: bold; display: block; margin-bottom: 8px; }
        input[type="text"] { width: 100%; padding: 12px; box-sizing: border-box; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; margin-bottom: 16px; }
        button { background-color: #1a73e8; color: white; border: none; padding: 14px; width: 100%; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; }
        button:active { background-color: #1557b0; }
        .result-box { margin-top: 20px; background: #f8f9fa; border: 1px solid #e1e4e8; padding: 16px; border-radius: 8px; white-space: pre-wrap; font-size: 15px; line-height: 1.5; }
        .loading { text-align: center; color: #666; font-style: italic; display: none; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🤖 Robô de Vendas & Copy</h2>
        <label for="tema">Qual o tema do seu produto ou post?</label>
        <input type="text" id="tema" placeholder="Ex: Tênis esportivo em promoção">
        <button onclick="gerarCopy()">Gerar Legenda com IA</button>
        <div id="loading" class="loading">Criando sua copy magnética... ⏳</div>
        <div id="resultado" class="result-box" style="display:none;"></div>
    </div>

    <script>
        async function gerarCopy() {
            const tema = document.getElementById('tema').value;
            const resultadoDiv = document.getElementById('resultado');
            const loadingDiv = document.getElementById('loading');
            
            if (!tema) {
                alert('Por favor, digite um tema!');
                return;
            }

            loadingDiv.style.display = 'block';
            resultadoDiv.style.display = 'none';

            try {
                const response = await fetch('/gerar-copy', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ tema: tema })
                });
                const data = await response.json();
                
                loadingDiv.style.display = 'none';
                if (data.status === 'sucesso') {
                    resultadoDiv.innerText = data.copy_gerada;
                    resultadoDiv.style.display = 'block';
                } else {
                    resultadoDiv.innerText = 'Erro ao gerar copy.';
                    resultadoDiv.style.display = 'block';
                }
            } catch (error) {
                loadingDiv.style.display = 'none';
                alert('Erro de conexão com o servidor.');
            }
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_PAGE)

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
