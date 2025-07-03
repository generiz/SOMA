from fastapi import APIRouter, Request, Query, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from app.utils.whatsapp_api import enviar_mensaje_whatsapp
from app.services.ia import generar_respuesta_ia
from app.database import get_db
from app.models.usuario import Usuario
from app.models.conversacion import Conversacion
import json
import os
from dotenv import load_dotenv

load_dotenv()

print("✅ CARGADO: webhook.py correcto")

router = APIRouter()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")  # Token para verificación inicial


# 🌐 Verificación del webhook con WhatsApp
@router.get("/webhook", response_class=PlainTextResponse)
async def verify_token(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
):
    print("🧪 LLEGÓ GET /webhook")
    print("🔍 VERIFICACIÓN")
    print("mode:", hub_mode)
    print("verify_token recibido:", repr(hub_verify_token))
    print("verify_token esperado:", repr(VERIFY_TOKEN))
    print("challenge:", hub_challenge)

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=hub_challenge, status_code=200)
    return PlainTextResponse(content="Invalid verification token", status_code=403)


# 📩 Recepción de mensajes de WhatsApp
@router.post("/webhook")
async def receive_message(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    print("📩 POST /webhook recibido")
    print(json.dumps(body, indent=2))

    try:
        entry = body["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        messages = value.get("messages")
        phone_id = value.get("metadata", {}).get("phone_number_id")

        if not phone_id:
            print("❌ phone_id no encontrado en metadata")
            return {"error": "phone_id faltante"}

        # 🔍 Buscar usuario por phone_id (empresa que recibió el mensaje)
        usuario = db.query(Usuario).filter(Usuario.phone_id == phone_id).first()
        if not usuario:
            print(f"❌ No se encontró un usuario registrado con phone_id: {phone_id}")
            return {"error": "usuario no encontrado"}

        if messages:
            msg = messages[0]
            numero_cliente = msg["from"]
            texto = msg["text"]["body"]
            print(f"💬 Mensaje recibido de {numero_cliente}: {texto}")

            # 🤖 Generar respuesta IA personalizada
            respuesta = generar_respuesta_ia(
                mensaje_usuario=texto,
                db=db,
                usuario_id=usuario.id,
                prompt_personalizado=usuario.prompt_personalizado,
            )
            print("🤖 Respuesta IA generada:", respuesta)

            # 📤 Enviar la respuesta al cliente
            enviar_mensaje_whatsapp(
                destinatario=numero_cliente,
                mensaje=respuesta,
                token=usuario.token_whatsapp,
                phone_id=usuario.phone_id,
            )

            # 💾 Guardar conversación
            conversacion = Conversacion(
                usuario_id=usuario.id,
                numero_cliente=numero_cliente,
                mensaje_cliente=texto,
                respuesta_ia=respuesta,
            )
            db.add(conversacion)
            db.commit()

    except Exception as e:
        print("❌ Error al procesar mensaje:", str(e))

    return {"status": "received"}
