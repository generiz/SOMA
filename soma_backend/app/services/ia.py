import os
import requests
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.models.producto import Producto

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def obtener_productos_para_prompt(db: Session):
    productos = db.query(Producto).filter(Producto.activo == True).all()
    return [
        {
            "nombre": p.nombre,
            "unidad": p.unidad,
            "precio_unitario": p.precio_unitario
        }
        for p in productos
    ]

def construir_prompt(cliente_msg: str, productos: list):
    lista_prod = "\n".join([
        f"- {p['nombre']} ({p['unidad']}): Gs. {p['precio_unitario']}" for p in productos
    ])

    prompt = f"""
Sos SOMA Assistant, el asistente de ventas de una tienda de alimentos saludables ubicada en Asunción, Paraguay.

Respondés con amabilidad, claridad y precisión. Tu objetivo es ayudar al cliente, recomendar productos si es posible, y facilitar la venta, no respondes nada que no tenga que ver con al tienda si te hacen una pregunta respondess "no puedo ayudarte con eso"

Lista actual de productos:
{lista_prod}

Información adicional:
- Horario: Lunes a Sábado de 9:00 a 19:00
- Formas de pago: Efectivo, Transferencia, QR
- Delivery propio, demora entre 30 y 60 minutos

Mensaje del cliente:
"{cliente_msg}"

Respondé como si fueras humano, profesional y cálido. Ofrecé ayuda útil y concreta. Si no entendés, pedí más información.
""".strip()

    return prompt

def generar_respuesta_ia(mensaje_usuario: str, db: Session) -> str:
    productos = obtener_productos_para_prompt(db)
    prompt = construir_prompt(mensaje_usuario, productos)

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {"role": "system", "content": "Sos un asistente de ventas para una tienda de alimentos."},
            {"role": "user", "content": prompt}
        ]
    }

    resp = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        raise RuntimeError(f"Error OpenRouter: {resp.status_code} {resp.text}") from e

    return resp.json()["choices"][0]["message"]["content"].strip()
