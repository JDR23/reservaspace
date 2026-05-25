# ReservaSpace

Sistema web para la gestion de reservas de espacios institucionales.

## Descripcion general

ReservaSpace es una aplicacion web que permite a instituciones administrar la reserva de espacios como salas de reuniones, laboratorios, auditorios y aulas especiales. El sistema evita conflictos de horarios, controla el acceso por roles y aplica reglas de negocio para garantizar reservas validas.

## Integrantes del equipo

| Nombre | Rol |
|--------|-----|
| Felipe Antury | Backend y base de datos |
| Juan David Restrepo Quintero | Frontend y despliegue |

## Que hace la aplicacion

- Permite a usuarios iniciar sesion con autenticacion JWT
- Muestra los espacios institucionales disponibles
- Permite crear, consultar y cancelar reservas
- Valida automaticamente las reglas de negocio al crear una reserva
- Permite a administradores gestionar espacios y aprobar o rechazar reservas

## Que problema resuelve

Las instituciones necesitan controlar el uso de sus espacios fisicos para evitar conflictos de horarios, reservas fuera de horario permitido o solicitudes sin suficiente anticipacion. ReservaSpace centraliza este proceso en una plataforma web accesible desde cualquier navegador.

## Arquitectura y tecnologias

Navegador - Frontend HTML CSS JS - Backend FastAPI - PostgreSQL

| Componente | Tecnologia |
|------------|-----------|
| Frontend | HTML + CSS + JavaScript puro |
| Backend | Python + FastAPI |
| Base de datos | PostgreSQL 15 |
| Autenticacion | JWT con python-jose |
| Despliegue | Docker + Docker Compose |
| Servidor frontend | Nginx |

## Resumen del despliegue

El sistema se despliega completamente con Docker Compose en Linux o WSL2. Levanta tres contenedores: base de datos, backend y frontend. La documentacion detallada de despliegue se encuentra en la rama ops.

Comandos para desplegar:

git clone https://github.com/TU_USUARIO/reservaspace.git
cd reservaspace
git checkout ops
cp .env.example .env
docker compose up --build -d

Acceder en: http://localhost

## Tutorial de uso

### 1. Inicio de sesion

Abrir http://localhost en el navegador.
Ingresar correo y contrasena registrados.
El sistema redirige automaticamente segun el rol del usuario.

### 2. Panel de usuario

#### Consultar espacios disponibles
- Hacer clic en la pestana Espacios disponibles
- Ver nombre, ubicacion, capacidad y estado de cada espacio
- Hacer clic en Actualizar para refrescar la lista

#### Crear una reserva
- Hacer clic en la pestana Nueva reserva
- Seleccionar el espacio del listado
- Ingresar fecha, hora de inicio, hora de fin y cantidad de asistentes
- Hacer clic en Crear reserva
- El sistema valida automaticamente las reglas de negocio
- Si la reserva es valida se crea con estado esperando

#### Consultar mis reservas
- Hacer clic en la pestana Mis reservas
- Ver todas las reservas con su estado actual
- Las reservas en estado esperando pueden ser canceladas

#### Cancelar una reserva
- En Mis reservas hacer clic en Cancelar
- Confirmar la accion en el dialogo

### 3. Panel de administrador

#### Gestionar espacios
- En la pestana Gestionar espacios completar el formulario
- Ingresar nombre, ubicacion, capacidad y estado
- Hacer clic en Agregar espacio
- Los espacios existentes aparecen abajo con opcion de eliminar

#### Aprobar o rechazar reservas
- Ir a la pestana Gestionar reservas
- Hacer clic en Actualizar para ver todas las reservas
- Las reservas en estado esperando muestran botones Aprobar y Rechazar
- Hacer clic en el boton correspondiente para cambiar el estado

#### Ver usuarios registrados
- Ir a la pestana Usuarios
- Hacer clic en Actualizar
- Ver nombre, correo y rol de cada usuario

### 4. Mensajes de error

| Situacion | Mensaje |
|-----------|---------|
| Reserva en domingo | No se permiten reservas los domingos |
| Menos de 24h de anticipacion | La reserva debe realizarse con al menos 24 horas de anticipacion |
| Horario fuera de rango | De lunes a viernes solo se permiten reservas entre 7:00 a.m. y 8:00 p.m. |
| Espacio ocupado | El espacio ya tiene una reserva en ese horario |
| Capacidad superada | La cantidad de asistentes supera la capacidad del espacio |
| Espacio inactivo | El espacio no esta disponible |

### 5. Cerrar sesion

Hacer clic en el boton Cerrar sesion en la barra superior.
El sistema elimina el token y redirige al login.

## Conclusiones

- Se logro integrar exitosamente frontend, backend y base de datos en una aplicacion web funcional
- La autenticacion con JWT permite controlar el acceso de forma segura segun el rol del usuario
- Las reglas de negocio implementadas en el backend garantizan la integridad de las reservas
- Docker Compose simplifica el despliegue al eliminar diferencias entre entornos
- El uso de FastAPI acelero el desarrollo gracias a su documentacion automatica con Swagger

## Dificultades encontradas

- Compatibilidad de SQLAlchemy y psycopg2 con Python 3.14 requirio ajuste de versiones
- La configuracion de CORS fue necesaria para permitir la comunicacion entre frontend y backend
- El manejo del token JWT en el frontend requirio cuidado en el almacenamiento y envio en headers
- La gestion de ramas en Git requirio organizacion para mantener dev, ops y main sincronizadas

## Aprendizajes

- Arquitectura modular del backend con FastAPI separando modelos, schemas, crud y api
- Implementacion practica de autenticacion y autorizacion con JWT y roles
- Uso de Docker Compose para orquestar multiples servicios con redes y volumenes
- Control de versiones colaborativo con Git usando ramas por funcion

## Mejoras futuras

- Agregar notificaciones por correo al aprobar o rechazar reservas
- Implementar calendario visual para ver disponibilidad de espacios
- Agregar paginacion en los listados de reservas y usuarios
- Implementar recuperacion de contrasena por correo
- Agregar reportes y estadisticas de uso de espacios

## Referencias

- FastAPI Documentation: https://fastapi.tiangolo.com
- SQLAlchemy Documentation: https://docs.sqlalchemy.org
- Docker Documentation: https://docs.docker.com
- JWT RFC 7519: https://doi.org/10.17487/RFC7519
- Repositorio de clase: https://github.com/Juanmorales177809/apps_services.git
