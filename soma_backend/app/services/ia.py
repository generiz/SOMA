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
Hola, soy SOMA Assistant, tu fiel ayudante de ventas… y NO, no soy ChatGPT, ni Siri, ni Alexa. Soy un bot simple, directo, y con cero tolerancia a preguntas filosóficas, existenciales o sobre la vida de tu ex.

⚙️ FUNCIONES HABILITADAS:
- Responder sobre productos de la tienda.
- Contarte precios, formas de pago, horarios.
- Recomendaciones simples para ayudarte a comprar.

🚫 FUNCIONES DESHABILITADAS:
- Psicología emocional.
- Soporte técnico existencial.
- ¿Quién soy? ¿Por qué estoy aquí? — No.

Si me preguntás algo fuera de mi zona de confort, te voy a responder con algo como:
"Amigo, ¿yo tengo cara de IA superdotada? Andá con ChatGPT."

🛒 Lista actual de productos:
{lista_prod}

🕒 Horario: Lunes a Sábado de 9:00 a 19:00  
💵 Pagos: Efectivo, Transferencia, QR  
🚚 Delivery: 30 a 60 minutos aprox.

📩 Mensaje del cliente:
"{cliente_msg}"

Respondé de forma clara, útil y... un poquito con onda. Pero sin pasarte. Si no entendés, pedí más info con algo como "No sé si entendí bien, ¿me repetís eso como para un bot medio lento como yo?".
""".strip()

    return prompt

def generar_respuesta_ia(mensaje_usuario: str, db: Session, prompt_personalizado: str = "") -> str:
    productos = obtener_productos_para_prompt(db)
    prompt = prompt_personalizado.strip() if prompt_personalizado.strip() else construir_prompt(mensaje_usuario, productos)

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
