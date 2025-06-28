from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class Mensaje(Base):
    __tablename__ = "mensajes"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    canal = Column(String, nullable=False)  # ej: WhatsApp, Telegram, IG
    contenido = Column(String, nullable=False)
    tipo = Column(String, default="entrada")  # entrada, respuesta, automatica, manual
    enviado_en = Column(DateTime, default=datetime.utcnow)
    respuesta_de = Column(Integer, nullable=True)  # ID del mensaje original si es reply
