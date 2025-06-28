from sqlalchemy.orm import Session
from app.models.mensaje import Mensaje
from app.schemas.mensaje import MensajeCreate, MensajeUpdate

def get_all(db: Session):
    return db.query(Mensaje).all()

def get_by_id(db: Session, mensaje_id: int):
    return db.query(Mensaje).filter(Mensaje.id == mensaje_id).first()

def create(db: Session, mensaje: MensajeCreate):
    nuevo = Mensaje(**mensaje.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def update(db: Session, mensaje_id: int, data: MensajeUpdate):
    db_mensaje = get_by_id(db, mensaje_id)
    if not db_mensaje:
        return None
    for key, value in data.dict().items():
        setattr(db_mensaje, key, value)
    db.commit()
    db.refresh(db_mensaje)
    return db_mensaje

def delete(db: Session, mensaje_id: int):
    db_mensaje = get_by_id(db, mensaje_id)
    if not db_mensaje:
        return None
    db.delete(db_mensaje)
    db.commit()
    return db_mensaje
