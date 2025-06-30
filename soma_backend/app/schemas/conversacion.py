from pydantic import BaseModel
from datetime import datetime

class ConversacionBase(BaseModel):
    numero_cliente: str
    mensaje_cliente: str
    respuesta_ia: str

class ConversacionCreate(ConversacionBase):
    usuario_id: int

class ConversacionOut(ConversacionBase):
    id: int
    usuario_id: int
    timestamp: datetime

    class Config:
        orm_mode = True
