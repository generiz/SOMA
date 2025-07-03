from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.ia import generar_respuesta_ia

router = APIRouter(prefix="/ia", tags=["IA"])


@router.post("/responder")
async def responder_mensaje(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    mensaje = data.get("mensaje", "")
    usuario_id = data.get("usuario_id")
    if not mensaje or usuario_id is None:
        return {"error": "Mensaje o usuario_id faltante"}

    respuesta = generar_respuesta_ia(mensaje, db, usuario_id)
    return {"respuesta": respuesta}
