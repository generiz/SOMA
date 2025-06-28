from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate

def get_all(db: Session):
    return db.query(Cliente).all()

def get_by_id(db: Session, cliente_id: int):
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()

def create(db: Session, cliente: ClienteCreate):
    nuevo = Cliente(**cliente.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def update(db: Session, cliente_id: int, data: ClienteUpdate):
    db_cliente = get_by_id(db, cliente_id)
    if not db_cliente:
        return None
    for key, value in data.dict().items():
        setattr(db_cliente, key, value)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def delete(db: Session, cliente_id: int):
    db_cliente = get_by_id(db, cliente_id)
    if not db_cliente:
        return None
    db.delete(db_cliente)
    db.commit()
    return db_cliente
