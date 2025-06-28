from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.detalle_pedido import DetallePedidoCreate, DetallePedidoOut, DetallePedidoUpdate
from app.crud import detalle_pedido as crud_detalle
from typing import List

router = APIRouter()

@router.get("/", response_model=List[DetallePedidoOut])
def listar_detalles(db: Session = Depends(get_db)):
    return crud_detalle.get_all(db)

@router.get("/{detalle_id}", response_model=DetallePedidoOut)
def obtener_detalle(detalle_id: int, db: Session = Depends(get_db)):
    detalle = crud_detalle.get_by_id(db, detalle_id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle

@router.post("/", response_model=DetallePedidoOut)
def crear_detalle(detalle: DetallePedidoCreate, db: Session = Depends(get_db)):
    return crud_detalle.create(db, detalle)

@router.put("/{detalle_id}", response_model=DetallePedidoOut)
def actualizar_detalle(detalle_id: int, data: DetallePedidoUpdate, db: Session = Depends(get_db)):
    actualizado = crud_detalle.update(db, detalle_id, data)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return actualizado

@router.delete("/{detalle_id}", response_model=DetallePedidoOut)
def eliminar_detalle(detalle_id: int, db: Session = Depends(get_db)):
    eliminado = crud_detalle.delete(db, detalle_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return eliminado
