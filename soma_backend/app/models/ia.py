from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.ia import generar_respuesta_ia

router = APIRouter(prefix="/ia", tags=["IA"])

@router.post("/responder")
def responder_mensaje(mensaje: str, db: Session = Depends(get_db)):
    respuesta = generar_respuesta_ia(mensaje, db)
    return {"respuesta": respuesta}
