import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cargar variables desde .env
load_dotenv()

# Obtener la URL de conexión
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise Exception("DATABASE_URL no definida en el entorno")

# Crear el engine (sin connect_args para PostgreSQL)
engine = create_engine(DATABASE_URL)

# Crear sesión y base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Crear tablas desde los modelos
def create_tables():
    from app.models import producto, cliente, pedido, detalle_pedido, mensaje, usuario
    Base.metadata.create_all(bind=engine)

# Dependency para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
