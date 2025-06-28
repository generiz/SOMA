from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import re

from app.database import get_db
from app.schemas.mensaje import MensajeCreate, MensajeOut, MensajeUpdate
from app.crud import mensaje as crud_mensaje
from app.models.producto import Producto
from app.models.mensaje import Mensaje
from app.services.ia import generar_respuesta_ia

router = APIRouter()

@router.get("/", response_model=List[MensajeOut])
def listar_mensajes(db: Session = Depends(get_db)):
    return crud_mensaje.get_all(db)

@router.get("/{mensaje_id}", response_model=MensajeOut)
def obtener_mensaje(mensaje_id: int, db: Session = Depends(get_db)):
    mensaje = crud_mensaje.get_by_id(db, mensaje_id)
    if not mensaje:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    return mensaje

@router.post("/", response_model=List[MensajeOut])
def crear_mensaje(mensaje: MensajeCreate, db: Session = Depends(get_db)):
    mensaje_guardado = crud_mensaje.create(db, mensaje)
    respuestas = [mensaje_guardado]

    if mensaje.tipo == "entrada":
        palabras = re.findall(r'\b\w+\b', mensaje.contenido.lower())
        productos = db.query(Producto).all()

        for producto in productos:
            if producto.nombre.lower() in palabras:
                try:
                    respuesta_texto = generar_respuesta_ia(
                        mensaje.contenido, producto.nombre, producto.precio_unitario
                    )
                except Exception as e:
                    print(f"[ERROR IA] {e}")
                    return respuestas

                mensaje_ia = MensajeCreate(
                    cliente_id=mensaje.cliente_id,
                    canal=mensaje.canal,
                    contenido=respuesta_texto,
                    tipo="automatica",
                    respuesta_de=mensaje_guardado.id
                )
                mensaje_respuesta = crud_mensaje.create(db, mensaje_ia)
                respuestas.append(mensaje_respuesta)
                break

    return respuestas

@router.put("/{mensaje_id}", response_model=MensajeOut)
def actualizar_mensaje(mensaje_id: int, data: MensajeUpdate, db: Session = Depends(get_db)):
    actualizado = crud_mensaje.update(db, mensaje_id, data)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    return actualizado

@router.delete("/{mensaje_id}", response_model=MensajeOut)
def eliminar_mensaje(mensaje_id: int, db: Session = Depends(get_db)):
    eliminado = crud_mensaje.delete(db, mensaje_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    return eliminado
