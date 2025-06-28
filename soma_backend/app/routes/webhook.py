from fastapi import APIRouter, Request, Query, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from app.utils.whatsapp_api import enviar_mensaje_whatsapp
from app.services.ia import generar_respuesta_ia
from app.database import get_db
import json
import os
from dotenv import load_dotenv

load_dotenv()

print("✅ CARGADO: webhook.py correcto")

router = APIRouter()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")  # ahora viene desde .env

@router.get("/webhook", response_class=PlainTextResponse)
async def verify_token(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    print("🔍 VERIFICACIÓN")
    print("mode:", hub_mode)
    print("verify_token recibido:", repr(hub_verify_token))
    print("verify_token esperado:", repr(VERIFY_TOKEN))
    print("challenge:", hub_challenge)

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=hub_challenge, status_code=200)
    return PlainTextResponse(content="Invalid verification token", status_code=403)

@router.post("/webhook")
async def receive_message(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    print("📩 POST /webhook recibido")
    print(json.dumps(body, indent=2))

    try:
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        messages = value.get('messages')

        if messages:
            msg = messages[0]
            numero = msg['from']
            texto = msg['text']['body']
            print(f"💬 Mensaje recibido de {numero}: {texto}")

            respuesta = generar_respuesta_ia(texto, db)
            print("🤖 Respuesta IA generada:", respuesta)

            enviar_mensaje_whatsapp(numero, respuesta)

    except Exception as e:
        print("❌ Error al procesar mensaje:", str(e))

    return {"status": "received"}
