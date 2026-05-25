from pydantic import BaseModel, Field
from typing import Literal

class EspacioCreate(BaseModel):
    nombre: str
    ubicacion: str
    capacidad: int = Field(gt=0)
    estado: Literal["activo", "inactivo", "en_mantenimiento", "no_disponible"] = "activo"

class EspacioUpdate(BaseModel):
    nombre: str | None = None
    ubicacion: str | None = None
    capacidad: int | None = None
    estado: Literal["activo", "inactivo", "en_mantenimiento", "no_disponible"] | None = None

class EspacioResponse(BaseModel):
    id_espacio: int
    nombre: str
    ubicacion: str
    capacidad: int
    estado: str

    class Config:
        from_attributes = True
