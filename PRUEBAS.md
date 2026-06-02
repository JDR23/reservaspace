# Casos de Prueba — ReservaSpace

## Pruebas de autenticacion

| Caso | Datos | Resultado esperado |
|------|-------|--------------------|
| Login correcto admin | admin@reservaspace.com / admin123 | Redirige a dashboard admin |
| Login correcto usuario | felipe@reservaspace.com / felipe123 | Redirige a dashboard usuario |
| Login incorrecto | cualquier@correo.com / mal | Error: correo o contrasena incorrectos |

## Pruebas de reglas de negocio

| Caso | Datos | Resultado esperado |
|------|-------|--------------------|
| Reserva en domingo | fecha domingo | Error: no se permiten reservas los domingos |
| Menos de 24h anticipacion | fecha de hoy | Error: minimo 24 horas de anticipacion |
| Hora inicio mayor a hora fin | inicio 10:00 fin 08:00 | Error: hora inicio debe ser anterior |
| Asistentes mayor a capacidad | 100 asistentes espacio cap 20 | Error: supera la capacidad |
| Espacio inactivo | espacio en mantenimiento | Error: espacio no disponible |
| Reserva valida | datos correctos | Reserva creada en estado esperando |

## Pruebas de roles

| Caso | Resultado esperado |
|------|--------------------|
| Usuario intenta aprobar reserva | Error 403 acceso denegado |
| Admin aprueba reserva | Estado cambia a aprobada |
| Admin rechaza reserva | Estado cambia a rechazada |
| Usuario cancela su reserva | Reserva eliminada correctamente |
