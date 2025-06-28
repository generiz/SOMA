from fastapi import FastAPI
from .database import create_tables
from .routes import producto, cliente, pedido, detalle_pedido, mensaje, ia, webhook
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="SOMA - Sistema Organizado de Mensajería y Automatización")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o ["http://localhost:3000"] si usás un puerto fijo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Crear tablas si no existen
create_tables()

# Incluir rutas principales
app.include_router(producto.router, prefix="/productos", tags=["Productos"])
app.include_router(cliente.router, prefix="/clientes", tags=["Clientes"])
app.include_router(pedido.router, prefix="/pedidos", tags=["Pedidos"])
app.include_router(detalle_pedido.router, prefix="/detalles", tags=["Detalles de pedido"])
app.include_router(mensaje.router, prefix="/mensajes", tags=["Mensajes"])
app.include_router(ia.router)
app.include_router(webhook.router)  # webhook para WhatsApp

# Ruta raíz para servir el frontend
@app.get("/")
def leer_panel():
    index_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "soma_frontend", "frontend", "index.html")
    )
    return FileResponse(index_path)


# Ruta de la base de datos (si la necesitás)
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(basedir, 'soma.db')}"
