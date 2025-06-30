from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nombre: str
    email: str
    numero_whatsapp: str
    token_whatsapp: str
    phone_id: str  # ✅ este campo es necesario
    prompt_personalizado: str = ""

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioOut(UsuarioBase):
    id: int

    class Config:
        orm_mode = True
