import os
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Robô de Copywriting</title>

<style>
body{
font-family:Arial,sans-serif;
background:#f4f4f4;
margin:0;
padding:20px;
}

.container{
max-width:600px;
margin:auto;
background:white;
padding:20px;
border-radius:10px;
box-shadow:0 0 10px rgba(0,0,0,.1);
}

input{
width:100%;
padding:12px;
margin:10px 0;
font-size:16px;
}

button{
width:100%;
padding:12px;
background:#1976d2;
color:white;
border:none;
border-radius:6px;
font-size:16px;
cursor:pointer;
}

button:hover{
background:#125ea8;
}

#resultado{
margin-top:20px;
white-space:pre-wrap;
background:#f7f7f7;
padding:15px;
border-radius:8px;
display:none;
}
</style>

</head>

<body>

<div class="container">

<h2>🤖 Robô de Vendas com IA</h2>

<input
id="tema"
placeholder="Digite o tema...">

<button onclick="gerarCopy()">

Gerar Copy

</button>

<div id="resultado"></div>

</div>

<script>

async function gerarCopy(){

const tema=document.getElementById("tema").value;

const resposta=await fetch("/gerar-copy",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
tema:tema
})

});

const dados=await resposta.json();

document.getElementById("resultado").style.display="block";

if(dados.status=="sucesso"){

document.getElementById("resultado").innerText=dados.copy;

}else{

document.getElementById("resultado").innerText=dados.mensagem;

}

}

</script>

</body>

</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)


@app.route("/gerar-copy", methods=["POST"])
def gerar():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return jsonify({
            "status":"erro",
            "mensagem":"A variável GEMINI_API_KEY não está configurada no Render."
        })

    tema = request.json.get("tema","")

    prompt = f"""
Crie uma legenda altamente persuasiva para Instagram.

Tema:

{tema}

Inclua:

• Emoji
• CTA
• 5 hashtags
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    payload = {
        "contents":[
            {
                "parts":[
                    {
                        "text":prompt
                    }
                ]
            }
        ]
    }

    resposta = requests.post(url,json=payload)

    if resposta.status_code != 200:

        return jsonify({

            "status":"erro",

            "mensagem":resposta.text

        })

    dados = resposta.json()

    texto = dados["candidates"][0]["content"]["parts"][0]["text"]

    return jsonify({

        "status":"sucesso",

        "copy":texto

    })


if __name__ == "__main__":

    porta=int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0",port=porta)
