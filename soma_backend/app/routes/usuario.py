from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.models.usuario import Usuario
from fastapi import HTTPException
from fastapi import HTTPException, Path
router = APIRouter()

@router.post("/", response_model=schemas.UsuarioOut)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(Usuario.numero_whatsapp == usuario.numero_whatsapp).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese número de WhatsApp.")
    
    nuevo = Usuario(**usuario.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[schemas.UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()


@router.delete("/{usuario_id}", response_model=schemas.UsuarioOut)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    db.delete(usuario)
    db.commit()
    return usuario
@router.put("/{usuario_id}", response_model=schemas.UsuarioOut)
def actualizar_usuario(usuario_id: int, datos_actualizados: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    for key, value in datos_actualizados.dict().items():
        setattr(usuario, key, value)

    db.commit()
    db.refresh(usuario)
    return usuario
