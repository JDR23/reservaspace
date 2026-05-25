from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status
from datetime import date, time, datetime, timedelta
from app.models.reserva import Reserva
from app.models.espacio import Espacio
from app.schemas.reserva import ReservaCreate, ReservaUpdateEstado

HORA_APERTURA_SEMANA = time(7, 0)
HORA_CIERRE_SEMANA = time(20, 0)
HORA_APERTURA_SABADO = time(8, 0)
HORA_CIERRE_SABADO = time(12, 0)

def validar_reglas_de_negocio(db: Session, datos: ReservaCreate, espacio: Espacio):
    if datos.hora_inicio >= datos.hora_fin:
        raise HTTPException(status_code=400, detail="La hora de inicio debe ser anterior a la hora de fin.")

    dia_semana = datos.fecha.weekday()
    if dia_semana == 6:
        raise HTTPException(status_code=400, detail="No se permiten reservas los domingos.")

    if dia_semana == 5:
        if datos.hora_inicio < HORA_APERTURA_SABADO or datos.hora_fin > HORA_CIERRE_SABADO:
            raise HTTPException(status_code=400, detail="Los sabados solo se permiten reservas entre 8:00 a.m. y 12:00 m.")
    else:
        if datos.hora_inicio < HORA_APERTURA_SEMANA or datos.hora_fin > HORA_CIERRE_SEMANA:
            raise HTTPException(status_code=400, detail="De lunes a viernes solo se permiten reservas entre 7:00 a.m. y 8:00 p.m.")

    fecha_hora_inicio = datetime.combine(datos.fecha, datos.hora_inicio)
    ahora = datetime.now()
    if fecha_hora_inicio - ahora < timedelta(hours=24):
        raise HTTPException(status_code=400, detail="La reserva debe realizarse con al menos 24 horas de anticipacion.")

    estados_bloqueados = ["inactivo", "en_mantenimiento", "no_disponible"]
    if espacio.estado in estados_bloqueados:
        raise HTTPException(status_code=400, detail=f"El espacio no esta disponible (estado: {espacio.estado}).")

    if datos.cantidad_asistentes > espacio.capacidad:
        raise HTTPException(status_code=400, detail=f"La cantidad de asistentes supera la capacidad del espacio ({espacio.capacidad}).")

    conflicto = db.query(Reserva).filter(
        and_(
            Reserva.id_espacio == datos.id_espacio,
            Reserva.fecha == datos.fecha,
            Reserva.estado != "rechazada",
            Reserva.hora_inicio < datos.hora_fin,
            Reserva.hora_fin > datos.hora_inicio
        )
    ).first()

    if conflicto:
        raise HTTPException(status_code=409, detail=f"El espacio ya tiene una reserva en ese horario (de {conflicto.hora_inicio} a {conflicto.hora_fin}).")

def crear_reserva(db: Session, datos: ReservaCreate, id_usuario: int) -> Reserva:
    espacio = db.query(Espacio).filter(Espacio.id_espacio == datos.id_espacio).first()
    if not espacio:
        raise HTTPException(status_code=404, detail="El espacio especificado no existe.")
    validar_reglas_de_negocio(db, datos, espacio)
    reserva = Reserva(
        id_usuario=id_usuario,
        id_espacio=datos.id_espacio,
        fecha=datos.fecha,
        hora_inicio=datos.hora_inicio,
        hora_fin=datos.hora_fin,
        cantidad_asistentes=datos.cantidad_asistentes,
        estado="esperando"
    )
    db.add(reserva)
    db.commit()
    db.refresh(reserva)
    return reserva

def obtener_reserva_por_id(db: Session, id_reserva: int):
    return db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()

def obtener_todas_las_reservas(db: Session):
    return db.query(Reserva).all()

def obtener_reservas_por_usuario(db: Session, id_usuario: int):
    return db.query(Reserva).filter(Reserva.id_usuario == id_usuario).all()

def actualizar_estado_reserva(db: Session, id_reserva: int, datos: ReservaUpdateEstado):
    reserva = obtener_reserva_por_id(db, id_reserva)
    if not reserva:
        return None
    reserva.estado = datos.estado
    db.commit()
    db.refresh(reserva)
    return reserva

def cancelar_reserva(db: Session, id_reserva: int, id_usuario: int) -> bool:
    reserva = db.query(Reserva).filter(
        and_(Reserva.id_reserva == id_reserva, Reserva.id_usuario == id_usuario)
    ).first()
    if not reserva:
        return False
    db.delete(reserva)
    db.commit()
    return True
