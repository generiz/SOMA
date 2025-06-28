from sqlalchemy import Column, Integer, Float, ForeignKey
from app.database import Base

class DetallePedido(Base):
    __tablename__ = "detalles_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Float, nullable=False)
    precio_unitario = Column(Float, nullable=False)  # Se congela en el momento del pedido
    subtotal = Column(Float, nullable=False)
