from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PedidoBase(BaseModel):
    cliente_id: int
    estado: Optional[str] = "pendiente"
    total: Optional[float] = 0.0

class PedidoCreate(PedidoBase):
    pass

class PedidoUpdate(PedidoBase):
    pass

class PedidoOut(PedidoBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime

    class Config:
        orm_mode = True
