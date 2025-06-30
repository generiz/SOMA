from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Conversacion(Base):
    __tablename__ = "conversaciones"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    numero_cliente = Column(String, nullable=False)
    mensaje_cliente = Column(String, nullable=False)
    respuesta_ia = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="conversaciones")
