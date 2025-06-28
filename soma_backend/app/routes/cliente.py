from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.cliente import ClienteCreate, ClienteOut, ClienteUpdate
from app.crud import cliente as crud_cliente
from typing import List

router = APIRouter()

@router.get("/", response_model=List[ClienteOut])
def listar_clientes(db: Session = Depends(get_db)):
    return crud_cliente.get_all(db)

@router.get("/{cliente_id}", response_model=ClienteOut)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = crud_cliente.get_by_id(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.post("/", response_model=ClienteOut)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return crud_cliente.create(db, cliente)

@router.put("/{cliente_id}", response_model=ClienteOut)
def actualizar_cliente(cliente_id: int, data: ClienteUpdate, db: Session = Depends(get_db)):
    actualizado = crud_cliente.update(db, cliente_id, data)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return actualizado

@router.delete("/{cliente_id}", response_model=ClienteOut)
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    eliminado = crud_cliente.delete(db, cliente_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return eliminado
