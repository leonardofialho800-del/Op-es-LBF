import os

from flask import Flask, request, jsonify, render_template_string
from google import genai

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Robô de Vendas IA</title>

<style>

body{
font-family:Arial;
background:#f5f5f5;
padding:25px;
}

.container{

max-width:650px;
margin:auto;
background:white;
padding:25px;
border-radius:10px;
box-shadow:0 0 10px rgba(0,0,0,.1);

}

input{

width:100%;
padding:12px;
font-size:16px;

}

button{

width:100%;
padding:14px;
margin-top:15px;
background:#1565C0;
color:white;
border:none;
font-size:16px;
cursor:pointer;

}

pre{

background:#eee;
padding:15px;
border-radius:8px;
white-space:pre-wrap;

}

</style>

</head>

<body>

<div class="container">

<h2>🤖 Robô de Vendas com IA</h2>

<input id="tema"
placeholder="Digite o tema">

<button onclick="gerar()">

Gerar Copy

</button>

<pre id="saida"></pre>

</div>

<script>

async function gerar(){

const tema=document.getElementById("tema").value;

const resposta=await fetch("/gerar-copy",{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify({

tema

})

});

const dados=await resposta.json();

document.getElementById("saida").textContent=dados.resultado || dados.erro;

}

</script>

</body>

</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/gerar-copy", methods=["POST"])
def gerar():

    try:

        api_key=os.environ["GEMINI_API_KEY"]

        client=genai.Client(api_key=api_key)

        tema=request.json.get("tema","")

        prompt=f"""

Crie uma legenda extremamente persuasiva para Instagram.

Tema:

{tema}

A resposta deve conter:

• Gancho forte

• Emojis

• CTA

• 5 hashtags

"""

        resposta=client.models.generate_content(

            model="gemini-2.5-flash",

            contents=prompt

        )

        return jsonify({

            "resultado":resposta.text

        })

    except Exception as e:

        return jsonify({

            "erro":str(e)

        })

if __name__=="__main__":

    porta=int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0",port=porta)
