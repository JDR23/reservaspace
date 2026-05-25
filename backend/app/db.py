"""
db.py — Configuración de la conexión a la base de datos
Usa SQLAlchemy como ORM y carga las variables de entorno desde .env
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

# URL de conexión a PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

# Motor de conexión
engine = create_engine(DATABASE_URL)

# Fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos ORM
Base = declarative_base()


def get_db():
    """
    Generador de sesión de base de datos.
    Se usa como dependencia en los endpoints de FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
