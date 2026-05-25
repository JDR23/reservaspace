"""
main.py — Punto de entrada principal de ReservaSpace
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.db import engine, Base

# Importar modelos para que SQLAlchemy los registre y cree las tablas
from app.models import usuario, espacio, reserva  # noqa: F401

load_dotenv()

# ── Crear tablas en la base de datos al iniciar ───────────────────────────────
Base.metadata.create_all(bind=engine)

# ── Instancia FastAPI ─────────────────────────────────────────────────────────
app = FastAPI(
    title="ReservaSpace API",
    description=(
        "API REST para la gestión de reservas de espacios institucionales. "
        "Permite administrar usuarios, espacios y reservas con autenticación JWT."
    ),
    version="1.0.0",
    contact={
        "name": "Felipe Antury & Juan David Restrepo",
    },
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/", tags=["Estado"])
def health_check():
    return {
        "status": "ok",
        "app": os.getenv("APP_NAME", "ReservaSpace"),
        "version": "1.0.0",
        "mensaje": "API de ReservaSpace funcionando correctamente"
    }

# ── Routers (se activarán en el siguiente paso) ───────────────────────────────
# from app.api import auth, usuarios, espacios, reservas
# app.include_router(auth.router,     prefix="/auth",     tags=["Autenticación"])
# app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
# app.include_router(espacios.router, prefix="/espacios", tags=["Espacios"])
# app.include_router(reservas.router, prefix="/reservas", tags=["Reservas"])
