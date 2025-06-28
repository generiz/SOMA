from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.ia import generar_respuesta_ia

router = APIRouter(prefix="/ia", tags=["IA"])

@router.post("/responder")
async def responder_mensaje(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    mensaje = data.get("mensaje", "")
    if not mensaje:
        return {"error": "Mensaje vacío"}

    respuesta = generar_respuesta_ia(mensaje, db)
    return {"respuesta": respuesta}
