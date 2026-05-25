"""
auth/jwt_handler.py — Manejo de JWT y autenticación
Contiene funciones para crear tokens, verificarlos y obtener el usuario actual
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from app.db import get_db
from app.models.usuario import Usuario

load_dotenv()

# ── Configuración ─────────────────────────────────────────────────────────────
SECRET_KEY                = os.getenv("SECRET_KEY", "clave_por_defecto")
ALGORITHM                 = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# ── Hash de contraseñas ───────────────────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ── Esquema OAuth2 — define de dónde se obtiene el token ─────────────────────
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hashear_contrasena(contrasena: str) -> str:
    """Genera el hash bcrypt de una contraseña en texto plano."""
    return pwd_context.hash(contrasena)


def verificar_contrasena(contrasena_plana: str, contrasena_hash: str) -> bool:
    """Compara contraseña en texto plano con su hash almacenado."""
    return pwd_context.verify(contrasena_plana, contrasena_hash)


def crear_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un JWT firmado con los datos del usuario.
    Incluye fecha de expiración automática.
    """
    payload = data.copy()
    expiracion = datetime.utcnow() + (
        expires_delta if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload.update({"exp": expiracion})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Dependencia de FastAPI: extrae y valida el token JWT.
    Retorna el usuario autenticado o lanza HTTPException 401.
    """
    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo: str = payload.get("sub")
        if correo is None:
            raise credenciales_exception
    except JWTError:
        raise credenciales_exception

    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if usuario is None:
        raise credenciales_exception

    return usuario


def requerir_admin(
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
) -> Usuario:
    """
    Dependencia de FastAPI: verifica que el usuario autenticado sea admin.
    Lanza HTTPException 403 si no tiene permiso.
    """
    if usuario_actual.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requiere rol de administrador."
        )
    return usuario_actual
