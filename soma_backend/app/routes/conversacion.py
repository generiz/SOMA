from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.conversacion import Conversacion
from app.schemas.conversacion import ConversacionOut

router = APIRouter()

@router.get("/conversaciones/", response_model=List[ConversacionOut])
def listar_conversaciones(db: Session = Depends(get_db)):
    return db.query(Conversacion).all()

@router.get("/conversaciones/cliente/{numero_cliente}", response_model=List[ConversacionOut])
def listar_por_numero(numero_cliente: str, db: Session = Depends(get_db)):
    return db.query(Conversacion).filter_by(numero_cliente=numero_cliente).all()

@router.get("/conversaciones/usuario/{usuario_id}", response_model=List[ConversacionOut])
def listar_por_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return db.query(Conversacion).filter_by(usuario_id=usuario_id).all()
