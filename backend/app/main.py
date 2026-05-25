from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.db import engine, Base
from app.models import usuario, espacio, reserva
from app.api import auth, usuarios, espacios, reservas

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ReservaSpace API",
    description="API REST para gestion de reservas de espacios institucionales.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,     prefix="/auth",     tags=["Autenticacion"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(espacios.router, prefix="/espacios", tags=["Espacios"])
app.include_router(reservas.router, prefix="/reservas", tags=["Reservas"])

@app.get("/", tags=["Estado"])
def health_check():
    return {
        "status": "ok",
        "app": os.getenv("APP_NAME", "ReservaSpace"),
        "version": "1.0.0",
        "mensaje": "API de ReservaSpace funcionando correctamente"
    }
