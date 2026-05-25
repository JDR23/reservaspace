from pydantic import BaseModel, EmailStr
from typing import Literal

class UsuarioCreate(BaseModel):
    nombre: str
    correo: EmailStr
    contrasena: str
    rol: Literal["admin", "usuario"] = "usuario"

class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    contrasena: str | None = None
    rol: Literal["admin", "usuario"] | None = None

class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre: str
    correo: str
    rol: str

    class Config:
        from_attributes = True
