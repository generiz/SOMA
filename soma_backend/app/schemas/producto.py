from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    unidad: str
    precio_unitario: float
    stock_actual: int
    stock_minimo: int
    activo: bool = True
    usuario_id: int


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(ProductoBase):
    pass


class ProductoOut(ProductoBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime

    class Config:
        orm_mode = True
