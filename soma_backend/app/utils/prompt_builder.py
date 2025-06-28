import os

def construir_prompt(cliente_msg, productos: list):
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompt_base.txt")
    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt_base = file.read()

    lista_prod = "\n".join([
        f"- {p['nombre']} ({p['unidad']}): Gs. {p['precio_unitario']}" for p in productos
    ])

    prompt = prompt_base.format(
        nombre_tienda="La Casa de la Comida",
        direccion="Mcal. López 1234, Asunción",
        horario="Lunes a Sábado, 9 a 19 hs",
        telefono="+595981123456",
        lista_productos_formateada=lista_prod,
        formas_de_pago="Efectivo, Transferencia, QR",
        info_delivery="Delivery propio, 30 a 60 minutos, Gs. 8.000 (gratis desde Gs. 100.000)"
    )

    prompt_final = f"{prompt}\n\nMensaje del cliente:\n\"{cliente_msg}\"\n\nRespuesta:"
    return prompt_final
