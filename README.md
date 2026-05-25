# ReservaSpace - Documentacion Tecnica (Rama dev)

## Integrantes

- Felipe Antury
- Juan David Restrepo Quintero

## Descripcion

ReservaSpace es una aplicacion web para gestionar reservas de espacios institucionales. Permite a usuarios autenticados consultar espacios y crear reservas, y a administradores gestionar espacios y aprobar o rechazar solicitudes.

## Arquitectura

El sistema sigue una arquitectura de tres capas:

- Frontend: HTML, CSS y JavaScript puro servido por Nginx
- Backend: API REST desarrollada con FastAPI en Python
- Base de datos: PostgreSQL gestionada con SQLAlchemy como ORM

## Estructura de carpetas

reservaspace/
├── backend/
│   ├── app/
│   │   ├── api/           # Endpoints REST
│   │   ├── models/        # Modelos ORM SQLAlchemy
│   │   ├── schemas/       # Validacion con Pydantic
│   │   ├── crud/          # Operaciones de base de datos
│   │   ├── auth/          # Manejo de JWT
│   │   ├── db.py          # Conexion a PostgreSQL
│   │   └── main.py        # Punto de entrada
│   └── requirements.txt
├── frontend/
│   ├── css/styles.css
│   ├── js/
│   │   ├── auth.js
│   │   ├── espacios.js
│   │   ├── reservas.js
│   │   └── admin.js
│   ├── login.html
│   ├── dashboard_usuario.html
│   └── dashboard_admin.html
└── docker-compose.yml

## Tecnologias utilizadas

| Componente | Tecnologia | Version |
|------------|-----------|---------|
| Frontend | HTML + CSS + JavaScript | ES6+ |
| Backend | FastAPI | 0.115.12 |
| ORM | SQLAlchemy | 2.0.40 |
| Base de datos | PostgreSQL | 15 |
| Autenticacion | python-jose JWT | 3.3.0 |
| Hash contrasenas | passlib bcrypt | 1.7.4 |
| Validacion | Pydantic | 2.13.4 |

## Modelo de base de datos

### Tabla usuarios
| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id_usuario | PK Integer | Identificador unico |
| nombre | String(100) | Nombre completo |
| correo | String(150) | Correo unico |
| contrasena | String(255) | Hash bcrypt |
| rol | String(20) | admin o usuario |

### Tabla espacios
| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id_espacio | PK Integer | Identificador unico |
| nombre | String(100) | Nombre del espacio |
| ubicacion | String(150) | Ubicacion fisica |
| capacidad | Integer | Maximo de personas |
| estado | String(30) | activo, inactivo, en_mantenimiento, no_disponible |

### Tabla reservas
| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id_reserva | PK Integer | Identificador unico |
| id_usuario | FK Integer | Referencia a usuarios |
| id_espacio | FK Integer | Referencia a espacios |
| fecha | Date | Fecha de la reserva |
| hora_inicio | Time | Hora de inicio |
| hora_fin | Time | Hora de fin |
| cantidad_asistentes | Integer | Numero de asistentes |
| estado | String(20) | esperando, aprobada, rechazada |

## Endpoints de la API

### Autenticacion
| Metodo | Endpoint | Descripcion | Acceso |
|--------|----------|-------------|--------|
| POST | /auth/login | Iniciar sesion | Publico |

### Usuarios
| Metodo | Endpoint | Descripcion | Acceso |
|--------|----------|-------------|--------|
| POST | /usuarios/ | Registrar usuario | Publico |
| GET | /usuarios/ | Listar usuarios | Admin |
| GET | /usuarios/me | Ver perfil propio | Autenticado |
| PUT | /usuarios/{id} | Actualizar usuario | Admin |
| DELETE | /usuarios/{id} | Eliminar usuario | Admin |

### Espacios
| Metodo | Endpoint | Descripcion | Acceso |
|--------|----------|-------------|--------|
| POST | /espacios/ | Crear espacio | Admin |
| GET | /espacios/ | Listar espacios | Autenticado |
| GET | /espacios/activos | Listar espacios activos | Autenticado |
| PUT | /espacios/{id} | Actualizar espacio | Admin |
| DELETE | /espacios/{id} | Eliminar espacio | Admin |

### Reservas
| Metodo | Endpoint | Descripcion | Acceso |
|--------|----------|-------------|--------|
| POST | /reservas/ | Crear reserva | Autenticado |
| GET | /reservas/ | Listar todas | Admin |
| GET | /reservas/mis-reservas | Ver mis reservas | Autenticado |
| PUT | /reservas/{id}/estado | Aprobar o rechazar | Admin |
| DELETE | /reservas/{id} | Cancelar reserva | Autenticado |

## Autenticacion JWT

1. El usuario envia correo y contrasena a POST /auth/login
2. El backend verifica credenciales y genera un token JWT
3. El token contiene correo, rol e id del usuario
4. El frontend guarda el token en sessionStorage
5. Cada peticion protegida envia el token en el header Authorization: Bearer token
6. El backend valida el token en cada request

### Roles
| Rol | Permisos |
|-----|----------|
| usuario | Consultar espacios, crear y cancelar sus reservas |
| admin | Todo lo anterior mas gestionar espacios y cambiar estado de reservas |

## Reglas de negocio implementadas

| ID | Regla |
|----|-------|
| A | Solo usuario autenticado puede crear reservas |
| B | Solo admin puede aprobar o rechazar reservas |
| C | No se permiten reservas en el mismo espacio, fecha y horario |
| D | Minimo 24 horas de anticipacion para crear una reserva |
| E | Horario permitido: Lu-Vi 7:00-20:00, Sa 8:00-12:00, Do no permitido |
| F | La hora de inicio debe ser anterior a la hora de fin |
| G | No se pueden reservar espacios inactivos o en mantenimiento |
| H | La cantidad de asistentes no puede superar la capacidad del espacio |
| I | Las reservas se crean en estado esperando, solo admin cambia el estado |

## Instrucciones para ejecutar en desarrollo

1. Clonar el repositorio
git clone https://github.com/JDR23/reservaspace.git
cd reservaspace
git checkout dev

2. Crear entorno virtual
cd backend
python3 -m venv venv
source venv/bin/activate

3. Instalar dependencias
pip install -r requirements.txt

4. Levantar base de datos con Docker
docker run --name reservaspace_db \
  -e POSTGRES_USER=reservaspace_user \
  -e POSTGRES_PASSWORD=reservaspace_pass \
  -e POSTGRES_DB=reservaspace_db \
  -p 5432:5432 -d postgres:15

5. Iniciar el backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

6. Abrir el frontend
Abrir frontend/login.html en el navegador
