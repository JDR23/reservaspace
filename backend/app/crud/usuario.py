from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.auth.jwt_handler import hashear_contrasena

def crear_usuario(db: Session, datos: UsuarioCreate) -> Usuario:
    usuario = Usuario(
        nombre=datos.nombre,
        correo=datos.correo,
        contrasena=hashear_contrasena(datos.contrasena),
        rol=datos.rol
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def obtener_usuario_por_id(db: Session, id_usuario: int):
    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

def obtener_usuario_por_correo(db: Session, correo: str):
    return db.query(Usuario).filter(Usuario.correo == correo).first()

def obtener_todos_los_usuarios(db: Session):
    return db.query(Usuario).all()

def actualizar_usuario(db: Session, id_usuario: int, datos: UsuarioUpdate):
    usuario = obtener_usuario_por_id(db, id_usuario)
    if not usuario:
        return None
    if datos.nombre:
        usuario.nombre = datos.nombre
    if datos.contrasena:
        usuario.contrasena = hashear_contrasena(datos.contrasena)
    if datos.rol:
        usuario.rol = datos.rol
    db.commit()
    db.refresh(usuario)
    return usuario

def eliminar_usuario(db: Session, id_usuario: int) -> bool:
    usuario = obtener_usuario_por_id(db, id_usuario)
    if not usuario:
        return False
    db.delete(usuario)
    db.commit()
    return True
