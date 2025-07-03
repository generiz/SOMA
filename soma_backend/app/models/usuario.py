from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False)
    numero_whatsapp = Column(String, nullable=False)
    token_whatsapp = Column(String, nullable=False)
    phone_id = Column(String, nullable=False)  # 🔹 agregado para usar en el webhook
    prompt_personalizado = Column(String, nullable=False)

    # 🔗 Relación con tabla conversaciones
    conversaciones = relationship(
        "Conversacion", back_populates="usuario", cascade="all, delete-orphan"
    )
    productos = relationship(
        "Producto", back_populates="usuario", cascade="all, delete-orphan"
    )
