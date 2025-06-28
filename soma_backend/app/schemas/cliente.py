from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClienteBase(BaseModel):
    nombre: str
    telefono: str
    direccion: Optional[str] = None
    notas: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    pass

class ClienteOut(ClienteBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime

    class Config:
        orm_mode = True
