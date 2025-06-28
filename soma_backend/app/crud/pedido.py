from sqlalchemy.orm import Session
from app.models.pedido import Pedido
from app.schemas.pedido import PedidoCreate, PedidoUpdate

def get_all(db: Session):
    return db.query(Pedido).all()

def get_by_id(db: Session, pedido_id: int):
    return db.query(Pedido).filter(Pedido.id == pedido_id).first()

def create(db: Session, pedido: PedidoCreate):
    nuevo = Pedido(**pedido.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def update(db: Session, pedido_id: int, data: PedidoUpdate):
    db_pedido = get_by_id(db, pedido_id)
    if not db_pedido:
        return None
    for key, value in data.dict().items():
        setattr(db_pedido, key, value)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def delete(db: Session, pedido_id: int):
    db_pedido = get_by_id(db, pedido_id)
    if not db_pedido:
        return None
    db.delete(db_pedido)
    db.commit()
    return db_pedido
