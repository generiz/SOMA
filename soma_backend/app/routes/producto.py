from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.producto import ProductoCreate, ProductoOut, ProductoUpdate
from app.crud import producto as crud_producto
from typing import List

router = APIRouter()

@router.get("/", response_model=List[ProductoOut])
def listar_productos(db: Session = Depends(get_db)):
    return crud_producto.get_all(db)

@router.get("/{producto_id}", response_model=ProductoOut)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = crud_producto.get_by_id(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.post("/", response_model=ProductoOut)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    return crud_producto.create(db, producto)

@router.put("/{producto_id}", response_model=ProductoOut)
def actualizar_producto(producto_id: int, data: ProductoUpdate, db: Session = Depends(get_db)):
    actualizado = crud_producto.update(db, producto_id, data)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return actualizado

@router.delete("/{producto_id}", response_model=ProductoOut)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    eliminado = crud_producto.delete(db, producto_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return eliminado
