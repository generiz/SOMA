from sqlalchemy.orm import Session
from app.models.producto import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate


def get_all(db: Session, usuario_id: int | None = None):
    query = db.query(Producto)
    if usuario_id is not None:
        query = query.filter(Producto.usuario_id == usuario_id)
    return query.all()


def get_by_id(db: Session, producto_id: int):
    return db.query(Producto).filter(Producto.id == producto_id).first()


def create(db: Session, producto: ProductoCreate):
    nuevo = Producto(**producto.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def update(db: Session, producto_id: int, data: ProductoUpdate):
    db_producto = get_by_id(db, producto_id)
    if not db_producto:
        return None
    for key, value in data.dict().items():
        setattr(db_producto, key, value)
    db.commit()
    db.refresh(db_producto)
    return db_producto


def delete(db: Session, producto_id: int):
    db_producto = get_by_id(db, producto_id)
    if not db_producto:
        return None
    db.delete(db_producto)
    db.commit()
    return db_producto
