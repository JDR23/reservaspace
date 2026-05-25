"""
models/usuario.py — Modelo ORM de la tabla usuarios
Define la estructura de la tabla en PostgreSQL usando SQLAlchemy
"""

from sqlalchemy import Column, Integer, String
from app.db import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario  = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre      = Column(String(100), nullable=False)
    correo      = Column(String(150), unique=True, nullable=False, index=True)
    contrasena  = Column(String(255), nullable=False)          # Hash bcrypt
    rol         = Column(String(20), nullable=False, default="usuario")  # admin / usuario
