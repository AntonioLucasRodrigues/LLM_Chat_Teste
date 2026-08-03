from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama

app = FastAPI(title="EcoLex API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MensagemUsuario(BaseModel):
    texto: str

@app.post("/chat")
async def responder_chat(mensagem: MensagemUsuario):
    # Essa função "yield" (entrega) pedacinho por pedacinho do texto
    def gerador_resposta():
        stream = ollama.chat(
            model='llama3',
            messages=[
                {"role": "system", "content": "Você é o EcoLex, especialista ambiental do PIM."},
                {"role": "user", "content": mensagem.texto}
            ],
            stream=True # Aqui ativamos o modo rápido!
        )
        
        for pedaco in stream:
            # Envia a palavra gerada imediatamente
            yield pedaco['message']['content']
            
        # Quando ele terminar de falar, colamos as fontes no finalzinho
        yield "<br><br><div style='font-size: 11px; color: #888; margin-top: 12px; border-top: 1px solid #eee; padding-top: 8px;'>Fontes: Resolução IPAAM 007/2015, Resolução CONAMA 237/1997</div>"
        
    return StreamingResponse(gerador_resposta(), media_type="text/plain")