from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.reserva import LoginSchema
from app.crud.usuario import obtener_usuario_por_correo
from app.auth.jwt_handler import verificar_contrasena, crear_token

router = APIRouter()

@router.post("/login", summary="Iniciar sesion")
def login(datos: LoginSchema, db: Session = Depends(get_db)):
    usuario = obtener_usuario_por_correo(db, datos.correo)
    if not usuario or not verificar_contrasena(datos.contrasena, usuario.contrasena):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contrasena incorrectos."
        )
    token = crear_token(data={
        "sub": usuario.correo,
        "rol": usuario.rol,
        "id": usuario.id_usuario
    })
    return {
        "access_token": token,
        "token_type": "bearer",
        "rol": usuario.rol,
        "nombre": usuario.nombre,
        "id_usuario": usuario.id_usuario
    }
