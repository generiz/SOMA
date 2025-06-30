from sqlalchemy.orm import Session
from app.models.usuario import Usuario

def get_usuario_por_numero(numero: str, db: Session) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.numero_whatsapp == numero).first()
