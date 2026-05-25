"""
main.py — Punto de entrada principal de la aplicación ReservaSpace
Configura FastAPI, registra los routers y define los metadatos de la API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# ── Crear instancia de FastAPI ────────────────────────────────────────────────
app = FastAPI(
    title="ReservaSpace API",
    description=(
        "API REST para la gestión de reservas de espacios institucionales. "
        "Permite administrar usuarios, espacios y reservas con autenticación JWT."
    ),
    version="1.0.0",
    contact={
        "name": "Felipe Antury & Juan David Restrepo",
        "email": "equipo@reservaspace.com",
    },
)

# ── Configuración de CORS ─────────────────────────────────────────────────────
# Permite que el frontend (HTML/JS) consuma la API desde el navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, reemplazar por el dominio real
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Ruta de salud (health check) ──────────────────────────────────────────────
@app.get("/", tags=["Estado"])
def health_check():
    """
    Endpoint de verificación: confirma que la API está activa.
    """
    return {
        "status": "ok",
        "app": os.getenv("APP_NAME", "ReservaSpace"),
        "version": "1.0.0",
        "mensaje": "API de ReservaSpace funcionando correctamente"
    }


# ── Registro de routers ───────────────────────────────────────────────────────
# Se irán importando a medida que se desarrolle cada módulo
# from app.api import auth, usuarios, espacios, reservas
# app.include_router(auth.router,      prefix="/auth",      tags=["Autenticación"])
# app.include_router(usuarios.router,  prefix="/usuarios",  tags=["Usuarios"])
# app.include_router(espacios.router,  prefix="/espacios",  tags=["Espacios"])
# app.include_router(reservas.router,  prefix="/reservas",  tags=["Reservas"])
