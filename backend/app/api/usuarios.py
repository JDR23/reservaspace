from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.crud.usuario import (
    crear_usuario, obtener_todos_los_usuarios,
    obtener_usuario_por_id, actualizar_usuario,
    eliminar_usuario, obtener_usuario_por_correo
)
from app.auth.jwt_handler import obtener_usuario_actual, requerir_admin
from app.models.usuario import Usuario

router = APIRouter()

@router.post("/", response_model=UsuarioResponse, status_code=201, summary="Registrar usuario")
def registrar_usuario(datos: UsuarioCreate, db: Session = Depends(get_db)):
    existente = obtener_usuario_por_correo(db, datos.correo)
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese correo.")
    return crear_usuario(db, datos)

@router.get("/", response_model=list[UsuarioResponse], summary="Listar usuarios (admin)")
def listar_usuarios(db: Session = Depends(get_db), admin: Usuario = Depends(requerir_admin)):
    return obtener_todos_los_usuarios(db)

@router.get("/me", response_model=UsuarioResponse, summary="Ver mi perfil")
def ver_mi_perfil(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    return usuario_actual

@router.get("/{id_usuario}", response_model=UsuarioResponse, summary="Ver usuario por ID (admin)")
def ver_usuario(id_usuario: int, db: Session = Depends(get_db), admin: Usuario = Depends(requerir_admin)):
    usuario = obtener_usuario_por_id(db, id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return usuario

@router.put("/{id_usuario}", response_model=UsuarioResponse, summary="Actualizar usuario (admin)")
def actualizar(id_usuario: int, datos: UsuarioUpdate, db: Session = Depends(get_db), admin: Usuario = Depends(requerir_admin)):
    usuario = actualizar_usuario(db, id_usuario, datos)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return usuario

@router.delete("/{id_usuario}", summary="Eliminar usuario (admin)")
def eliminar(id_usuario: int, db: Session = Depends(get_db), admin: Usuario = Depends(requerir_admin)):
    eliminado = eliminar_usuario(db, id_usuario)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return {"mensaje": "Usuario eliminado correctamente."}
