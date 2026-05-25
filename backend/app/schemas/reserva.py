from pydantic import BaseModel, Field
from typing import Literal
from datetime import date, time

class ReservaCreate(BaseModel):
    id_espacio: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    cantidad_asistentes: int = Field(gt=0)

class ReservaUpdateEstado(BaseModel):
    estado: Literal["aprobada", "rechazada"]

class ReservaResponse(BaseModel):
    id_reserva: int
    id_usuario: int
    id_espacio: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    cantidad_asistentes: int
    estado: str

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    correo: str
    contrasena: str
