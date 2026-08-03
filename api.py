# api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama

app = FastAPI(title="EcoLex API")

# Isso permite que o seu site HTML converse com o Python localmente
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Na produção, colocamos a URL real do site
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estrutura da mensagem que o frontend vai enviar
class MensagemUsuario(BaseModel):
    texto: str

@app.post("/chat")
def responder_chat(mensagem: MensagemUsuario):
    # Aqui o Python recebe o texto do HTML e manda pro Ollama
    resposta_ollama = ollama.chat(
        model='llama3',
        messages=[
            {"role": "system", "content": "Você é o EcoLex, especialista ambiental do PIM."},
            {"role": "user", "content": mensagem.texto}
        ]
    )
    
    # Devolve a resposta para o site
    return {
        "resposta": resposta_ollama['message']['content'],
        "fontes": ["Resolução IPAAM 007/2015"] # Simulação do RAG
    }