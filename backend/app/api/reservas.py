from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.reserva import ReservaCreate, ReservaUpdateEstado, ReservaResponse
from app.crud.reserva import (
    crear_reserva, obtener_todas_las_reservas,
    obtener_reservas_por_usuario, obtener_reserva_por_id,
    actualizar_estado_reserva, cancelar_reserva
)
from app.auth.jwt_handler import obtener_usuario_actual, requerir_admin
from app.models.usuario import Usuario

router = APIRouter()

@router.post("/", response_model=ReservaResponse, status_code=201, summary="Crear reserva")
def crear(datos: ReservaCreate, db: Session = Depends(get_db), usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    return crear_reserva(db, datos, usuario_actual.id_usuario)

@router.get("/", response_model=list[ReservaResponse], summary="Listar todas las reservas (admin)")
def listar_todas(db: Session = Depends(get_db), admin: Usuario = Depends(requerir_admin)):
    return obtener_todas_las_reservas(db)

@router.get("/mis-reservas", response_model=list[ReservaResponse], summary="Ver mis reservas")
def mis_reservas(db: Session = Depends(get_db), usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    return obtener_reservas_por_usuario(db, usuario_actual.id_usuario)

@router.get("/{id_reserva}", response_model=ReservaResponse, summary="Ver reserva por ID")
def ver_reserva(id_reserva: int, db: Session = Depends(get_db), usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    reserva = obtener_reserva_por_id(db, id_reserva)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada.")
    return reserva

@router.put("/{id_reserva}/estado", response_model=ReservaResponse, summary="Actualizar estado (admin)")
def actualizar_estado(id_reserva: int, datos: ReservaUpdateEstado, db: Session = Depends(get_db), admin: Usuario = Depends(requerir_admin)):
    reserva = actualizar_estado_reserva(db, id_reserva, datos)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada.")
    return reserva

@router.delete("/{id_reserva}", summary="Cancelar reserva")
def cancelar(id_reserva: int, db: Session = Depends(get_db), usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    cancelado = cancelar_reserva(db, id_reserva, usuario_actual.id_usuario)
    if not cancelado:
        raise HTTPException(status_code=404, detail="Reserva no encontrada o sin permiso.")
    return {"mensaje": "Reserva cancelada correctamente."}
