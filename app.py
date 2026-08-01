import os
from flask import Flask, request, jsonify, render_template_string
from google import genai

API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBrhs-bTh4gyx35cQEvGYfmg1oa2jqhbKg")
client = genai.Client(api_key=API_KEY)

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Robô de Copywriting - LBF</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; color: #333; }
        .container { max-width: 500px; margin: 40px auto; background: #fff; padding: 24px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        h2 { text-align: center; color: #1a73e8; margin-bottom: 20px; }
        label { font-weight: bold; display: block; margin-bottom: 8px; }
        input[type="text"] { width: 100%; padding: 12px; box-sizing: border-box; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; margin-bottom: 16px; }
        button { background-color: #1a73e8; color: white; border: none; padding: 14px; width: 100%; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: background 0.2s; }
        button:hover { background-color: #1557b0; }
        .result-box { margin-top: 20px; background: #f8f9fa; border: 1px solid #e1e4e8; padding: 16px; border-radius: 8px; white-space: pre-wrap; font-size: 15px; line-height: 1.5; }
        .error-box { margin-top: 20px; background: #fde8e8; border: 1px solid #f8b4b4; color: #c53030; padding: 16px; border-radius: 8px; font-size: 14px; display: none; word-break: break-all; }
        .loading { text-align: center; color: #d97706; font-weight: 500; font-size: 14px; display: none; margin-top: 15px; background: #fef3c7; padding: 10px; border-radius: 6px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🤖 Robô de Vendas & Copy</h2>
        <label for="tema">Qual o tema do seu produto ou post?</label>
        <input type="text" id="tema" placeholder="Ex: Tênis esportivo em promoção">
        <button onclick="gerarCopy()">Gerar Legenda com IA</button>
        <div id="loading" class="loading">⏳ Gerando sua copy com Gemini 2.5 Flash...</div>
        <div id="resultado" class="result-box" style="display:none;"></div>
        <div id="erro" class="error-box"></div>
    </div>

    <script>
        async function gerarCopy() {
            const tema = document.getElementById('tema').value;
            const resultadoDiv = document.getElementById('resultado');
            const erroDiv = document.getElementById('erro');
            const loadingDiv = document.getElementById('loading');
            
            if (!tema) {
                alert('Por favor, digite um tema!');
                return;
            }

            loadingDiv.style.display = 'block';
            resultadoDiv.style.display = 'none';
            erroDiv.style.display = 'none';

            try {
                const response = await fetch('/gerar-copy', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ tema: tema })
                });
                const data = await response.json();
                
                loadingDiv.style.display = 'none';
                if (response.ok && data.status === 'sucesso') {
                    resultadoDiv.innerText = data.copy_gerada;
                    resultadoDiv.style.display = 'block';
                } else {
                    erroDiv.innerText = 'Erro: ' + (data.mensagem || 'Desconhecido');
                    erroDiv.style.display = 'block';
                }
            } catch (error) {
                loadingDiv.style.display = 'none';
                erroDiv.innerText = 'Erro de conexão com o servidor.';
                erroDiv.style.display = 'block';
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
    try:
        dados = request.json
        tema = dados.get('tema')
        
        if not tema:
            return jsonify({"status": "erro", "mensagem": "O tema não pode estar vazio."}), 400
            
        prompt = f"Escreva uma legenda persuasiva e profissional para o Instagram sobre o seguinte tema: {tema}. Inclua 5 hashtags."
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        return jsonify({
            "status": "sucesso",
            "tema_pedido": tema,
            "copy_gerada": response.text
        })
    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
