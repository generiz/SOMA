from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MensajeBase(BaseModel):
    cliente_id: int
    canal: str
    contenido: str
    tipo: Optional[str] = "entrada"
    respuesta_de: Optional[int] = None

class MensajeCreate(MensajeBase):
    pass

class MensajeUpdate(MensajeBase):
    pass

class MensajeOut(MensajeBase):
    id: int
    enviado_en: datetime

    class Config:
        orm_mode = True
