# ReservaSpace - Documentacion de Despliegue (Rama ops)

## Integrantes

- Felipe Antury
- Juan David Restrepo Quintero

## Requisitos previos

| Herramienta | Version minima |
|-------------|---------------|
| Docker | 24.0 o superior |
| Docker Compose | 2.0 o superior |
| Git | 2.x |
| WSL2 con Ubuntu | Windows 11 si aplica |

Verificar instalacion:

docker --version
docker compose version
git --version

## Clonar el repositorio

git clone https://github.com/JDR23/reservaspace.git
cd reservaspace
git checkout ops

## Configuracion de variables de entorno

cp .env.example .env

Contenido del archivo .env:

POSTGRES_USER=reservaspace_user
POSTGRES_PASSWORD=reservaspace_pass
POSTGRES_DB=reservaspace_db
DATABASE_URL=postgresql://reservaspace_user:reservaspace_pass@db:5432/reservaspace_db
SECRET_KEY=clave_secreta_super_segura_reservaspace_2024
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
APP_NAME=ReservaSpace

## Explicacion de variables de entorno

| Variable | Descripcion |
|----------|-------------|
| POSTGRES_USER | Usuario de PostgreSQL |
| POSTGRES_PASSWORD | Contrasena de PostgreSQL |
| POSTGRES_DB | Nombre de la base de datos |
| DATABASE_URL | URL completa de conexion al backend |
| SECRET_KEY | Clave para firmar los tokens JWT |
| ALGORITHM | Algoritmo de firma JWT |
| ACCESS_TOKEN_EXPIRE_MINUTES | Duracion del token en minutos |
| APP_NAME | Nombre de la aplicacion |

## Dockerfile del backend

FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

## Dockerfile del frontend

FROM nginx:alpine
RUN rm -rf /usr/share/nginx/html/*
COPY . /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

## Puertos utilizados

| Servicio | Puerto |
|----------|--------|
| Frontend Nginx | 80 |
| Backend FastAPI | 8000 |
| Base de datos PostgreSQL | 5432 |

## Construccion y ejecucion

Construir y levantar en segundo plano:
docker compose up --build -d

Ver logs en tiempo real:
docker compose logs -f

Ver logs de un servicio especifico:
docker compose logs -f backend
docker compose logs -f db
docker compose logs -f frontend

Verificar contenedores corriendo:
docker ps

## Verificacion del sistema

| URL | Resultado esperado |
|-----|-------------------|
| http://localhost | Pantalla de login |
| http://localhost:8000 | JSON con status ok |
| http://localhost:8000/docs | Swagger UI |

## Apagado y reinicio

Apagar sin eliminar datos:
docker compose down

Apagar y eliminar base de datos:
docker compose down -v

Reiniciar un servicio:
docker compose restart backend

Reconstruir y reiniciar:
docker compose up --build -d

## Actualizacion del sistema

git pull origin ops
docker compose down
docker compose up --build -d

## Solucion de errores comunes

Error: Connection refused al backend
- Verificar que el contenedor esta corriendo con docker ps
- Ver logs con docker compose logs backend

Error: psycopg2 module not found
- Reconstruir la imagen con docker compose up --build

Error: Port 80 already in use
- Identificar el proceso con sudo lsof -i :80
- Cambiar el puerto en docker-compose.yml a 8080:80

Error: database does not exist
- Eliminar volumen y recrear con docker compose down -v
- Luego docker compose up --build

El frontend no se conecta al backend
- Verificar que en frontend/js/auth.js la variable API sea http://localhost:8000
