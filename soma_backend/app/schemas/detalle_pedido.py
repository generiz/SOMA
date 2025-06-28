from pydantic import BaseModel

class DetallePedidoBase(BaseModel):
    pedido_id: int
    producto_id: int
    cantidad: float
    precio_unitario: float
    subtotal: float

class DetallePedidoCreate(DetallePedidoBase):
    pass

class DetallePedidoUpdate(DetallePedidoBase):
    pass

class DetallePedidoOut(DetallePedidoBase):
    id: int

    class Config:
        orm_mode = True
