"""
schemas/usuario.py — Esquemas Pydantic para validación de datos de usuarios
Separa los datos de entrada, salida y creación
"""

from pydantic import BaseModel, EmailStr
from typing import Literal


# ── Creación de usuario (entrada) ─────────────────────────────────────────────
class UsuarioCreate(BaseModel):
    nombre:     str
    correo:     EmailStr
    contrasena: str
    rol:        Literal["admin", "usuario"] = "usuario"


# ── Actualización parcial ─────────────────────────────────────────────────────
class UsuarioUpdate(BaseModel):
    nombre:     str | None = None
    contrasena: str | None = None
    rol:        Literal["admin", "usuario"] | None = None


# ── Respuesta (salida) — nunca expone la contraseña ───────────────────────────
class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre:     str
    correo:     str
    rol:        str

    class Config:
        from_attributes = True  # Permite convertir objetos ORM a JSON
