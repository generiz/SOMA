import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_DEFECTO = os.getenv("WHATSAPP_TOKEN")
PHONE_ID_DEFECTO = os.getenv("WHATSAPP_PHONE_ID")

def enviar_mensaje_whatsapp(destinatario: str, mensaje: str, token=None, phone_id=None):
    token = token or TOKEN_DEFECTO
    phone_id = phone_id or PHONE_ID_DEFECTO

    url = f"https://graph.facebook.com/v18.0/{phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": destinatario,
        "type": "text",
        "text": {"body": mensaje}
    }

    response = requests.post(url, headers=headers, json=payload)
    print(f"📤 STATUS: {response.status_code}")
    print(f"📤 RESPONSE: {response.text}")


