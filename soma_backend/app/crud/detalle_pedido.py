from sqlalchemy.orm import Session
from app.models.detalle_pedido import DetallePedido
from app.schemas.detalle_pedido import DetallePedidoCreate, DetallePedidoUpdate

def get_all(db: Session):
    return db.query(DetallePedido).all()

def get_by_id(db: Session, detalle_id: int):
    return db.query(DetallePedido).filter(DetallePedido.id == detalle_id).first()

def create(db: Session, detalle: DetallePedidoCreate):
    nuevo = DetallePedido(**detalle.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def update(db: Session, detalle_id: int, data: DetallePedidoUpdate):
    db_detalle = get_by_id(db, detalle_id)
    if not db_detalle:
        return None
    for key, value in data.dict().items():
        setattr(db_detalle, key, value)
    db.commit()
    db.refresh(db_detalle)
    return db_detalle

def delete(db: Session, detalle_id: int):
    db_detalle = get_by_id(db, detalle_id)
    if not db_detalle:
        return None
    db.delete(db_detalle)
    db.commit()
    return db_detalle
