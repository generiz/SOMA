from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.pedido import PedidoCreate, PedidoOut, PedidoUpdate
from app.crud import pedido as crud_pedido
from typing import List

router = APIRouter()

@router.get("/", response_model=List[PedidoOut])
def listar_pedidos(db: Session = Depends(get_db)):
    return crud_pedido.get_all(db)

@router.get("/{pedido_id}", response_model=PedidoOut)
def obtener_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = crud_pedido.get_by_id(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

@router.post("/", response_model=PedidoOut)
def crear_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    return crud_pedido.create(db, pedido)

@router.put("/{pedido_id}", response_model=PedidoOut)
def actualizar_pedido(pedido_id: int, data: PedidoUpdate, db: Session = Depends(get_db)):
    actualizado = crud_pedido.update(db, pedido_id, data)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return actualizado

@router.delete("/{pedido_id}", response_model=PedidoOut)
def eliminar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    eliminado = crud_pedido.delete(db, pedido_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return eliminado
