from sqlalchemy.orm import Session
from app.models.espacio import Espacio
from app.schemas.espacio import EspacioCreate, EspacioUpdate

def crear_espacio(db: Session, datos: EspacioCreate) -> Espacio:
    espacio = Espacio(
        nombre=datos.nombre,
        ubicacion=datos.ubicacion,
        capacidad=datos.capacidad,
        estado=datos.estado
    )
    db.add(espacio)
    db.commit()
    db.refresh(espacio)
    return espacio

def obtener_espacio_por_id(db: Session, id_espacio: int):
    return db.query(Espacio).filter(Espacio.id_espacio == id_espacio).first()

def obtener_todos_los_espacios(db: Session):
    return db.query(Espacio).all()

def obtener_espacios_activos(db: Session):
    return db.query(Espacio).filter(Espacio.estado == "activo").all()

def actualizar_espacio(db: Session, id_espacio: int, datos: EspacioUpdate):
    espacio = obtener_espacio_por_id(db, id_espacio)
    if not espacio:
        return None
    if datos.nombre is not None:
        espacio.nombre = datos.nombre
    if datos.ubicacion is not None:
        espacio.ubicacion = datos.ubicacion
    if datos.capacidad is not None:
        espacio.capacidad = datos.capacidad
    if datos.estado is not None:
        espacio.estado = datos.estado
    db.commit()
    db.refresh(espacio)
    return espacio

def eliminar_espacio(db: Session, id_espacio: int) -> bool:
    espacio = obtener_espacio_por_id(db, id_espacio)
    if not espacio:
        return False
    db.delete(espacio)
    db.commit()
    return True
