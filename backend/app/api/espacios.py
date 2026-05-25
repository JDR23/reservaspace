from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.espacio import EspacioCreate, EspacioUpdate, EspacioResponse
from app.crud.espacio import (
    crear_espacio, obtener_todos_los_espacios, obtener_espacios_activos,
    obtener_espacio_por_id, actualizar_espacio, eliminar_espacio
)
from app.auth.jwt_handler import obtener_usuario_actual, requerir_admin
from app.models.usuario import Usuario

router = APIRouter()

@router.post("/", response_model=EspacioResponse, status_code=201, summary="Crear espacio (admin)")
def crear(datos: EspacioCreate, db: Session = Depends(get_db), admin: Usuario = Depends(requerir_admin)):
    return crear_espacio(db, datos)

@router.get("/", response_model=list[EspacioResponse], summary="Listar todos los espacios")
def listar_espacios(db: Session = Depends(get_db), usuario: Usuario = Depends(obtener_usuario_actual)):
    return obtener_todos_los_espacios(db)

@router.get("/activos", response_model=list[EspacioResponse], summary="Listar espacios activos")
def listar_activos(db: Session = Depends(get_db), usuario: Usuario = Depends(obtener_usuario_actual)):
    return obtener_espacios_activos(db)

@router.get("/{id_espacio}", response_model=EspacioResponse, summary="Ver espacio por ID")
def ver_espacio(id_espacio: int, db: Session = Depends(get_db), usuario: Usuario = Depends(obtener_usuario_actual)):
    espacio = obtener_espacio_por_id(db, id_espacio)
    if not espacio:
        raise HTTPException(status_code=404, detail="Espacio no encontrado.")
    return espacio

@router.put("/{id_espacio}", response_model=EspacioResponse, summary="Actualizar espacio (admin)")
def actualizar(id_espacio: int, datos: EspacioUpdate, db: Session = Depends(get_db), admin: Usuario = Depends(requerir_admin)):
    espacio = actualizar_espacio(db, id_espacio, datos)
    if not espacio:
        raise HTTPException(status_code=404, detail="Espacio no encontrado.")
    return espacio

@router.delete("/{id_espacio}", summary="Eliminar espacio (admin)")
def eliminar(id_espacio: int, db: Session = Depends(get_db), admin: Usuario = Depends(requerir_admin)):
    eliminado = eliminar_espacio(db, id_espacio)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Espacio no encontrado.")
    return {"mensaje": "Espacio eliminado correctamente."}
