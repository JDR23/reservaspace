// Verificar que sea admin
verificarAuth("admin");

async function cargarEspaciosAdmin() {
  const token = getToken();
  const contenedor = document.getElementById("listaEspaciosAdmin");
  contenedor.innerHTML = "<p>Cargando...</p>";

  try {
    const res = await fetch(`${API}/espacios/`, {
      headers: { "Authorization": `Bearer ${token}` }
    });
    const espacios = await res.json();

    if (!espacios.length) {
      contenedor.innerHTML = "<p>No hay espacios registrados.</p>";
      return;
    }

    contenedor.innerHTML = espacios.map(e => `
      <div class="card">
        <h3>🏢 ${e.nombre}</h3>
        <p>📍 ${e.ubicacion}</p>
        <p>👥 Capacidad: ${e.capacidad}</p>
        <p>Estado: <span class="estado-${e.estado}">${e.estado}</span></p>
        <div class="card-actions">
          <button class="btn-danger" onclick="eliminarEspacio(${e.id_espacio})">
            Eliminar
          </button>
        </div>
      </div>
    `).join("");

  } catch (err) {
    contenedor.innerHTML = "<p>Error al cargar espacios.</p>";
  }
}

async function eliminarEspacio(id) {
  if (!confirm("¿Eliminar este espacio?")) return;
  const token = getToken();

  const res = await fetch(`${API}/espacios/${id}`, {
    method: "DELETE",
    headers: { "Authorization": `Bearer ${token}` }
  });

  if (res.ok) {
    alert("Espacio eliminado.");
    cargarEspaciosAdmin();
  } else {
    alert("No se pudo eliminar el espacio.");
  }
}

async function cargarTodasReservas() {
  const token = getToken();
  const contenedor = document.getElementById("listaTodasReservas");
  contenedor.innerHTML = "<p>Cargando...</p>";

  try {
    const res = await fetch(`${API}/reservas/`, {
      headers: { "Authorization": `Bearer ${token}` }
    });
    const reservas = await res.json();

    if (!reservas.length) {
      contenedor.innerHTML = "<p>No hay reservas registradas.</p>";
      return;
    }

    contenedor.innerHTML = reservas.map(r => `
      <div class="card">
        <h3>📅 Reserva #${r.id_reserva}</h3>
        <p>👤 Usuario ID: ${r.id_usuario}</p>
        <p>🏢 Espacio ID: ${r.id_espacio}</p>
        <p>📆 Fecha: ${r.fecha}</p>
        <p>🕐 Horario: ${r.hora_inicio} - ${r.hora_fin}</p>
        <p>👥 Asistentes: ${r.cantidad_asistentes}</p>
        <p>Estado: <span class="estado-${r.estado}">${r.estado}</span></p>
        <div class="card-actions">
          ${r.estado === "esperando" ? `
            <button class="btn-success" onclick="cambiarEstado(${r.id_reserva}, 'aprobada')">
              Aprobar
            </button>
            <button class="btn-danger" onclick="cambiarEstado(${r.id_reserva}, 'rechazada')">
              Rechazar
            </button>` : ""}
        </div>
      </div>
    `).join("");

  } catch (err) {
    contenedor.innerHTML = "<p>Error al cargar reservas.</p>";
  }
}

async function cambiarEstado(id, estado) {
  const token = getToken();

  const res = await fetch(`${API}/reservas/${id}/estado`, {
    method: "PUT",
    headers: {
      "Content-Type":  "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({ estado })
  });

  if (res.ok) {
    alert(`Reserva ${estado} correctamente.`);
    cargarTodasReservas();
  } else {
    alert("No se pudo actualizar el estado.");
  }
}

async function cargarUsuarios() {
  const token = getToken();
  const contenedor = document.getElementById("listaUsuarios");
  contenedor.innerHTML = "<p>Cargando...</p>";

  try {
    const res = await fetch(`${API}/usuarios/`, {
      headers: { "Authorization": `Bearer ${token}` }
    });
    const usuarios = await res.json();

    contenedor.innerHTML = usuarios.map(u => `
      <div class="card">
        <h3>👤 ${u.nombre}</h3>
        <p>📧 ${u.correo}</p>
        <p>Rol: <span class="badge badge-${u.rol}">${u.rol}</span></p>
      </div>
    `).join("");

  } catch (err) {
    contenedor.innerHTML = "<p>Error al cargar usuarios.</p>";
  }
}

// Formulario de nuevo espacio
const formEspacio = document.getElementById("formEspacio");
if (formEspacio) {
  formEspacio.addEventListener("submit", async (e) => {
    e.preventDefault();
    const token = getToken();

    const datos = {
      nombre:    document.getElementById("esp_nombre").value,
      ubicacion: document.getElementById("esp_ubicacion").value,
      capacidad: parseInt(document.getElementById("esp_capacidad").value),
      estado:    document.getElementById("esp_estado").value
    };

    try {
      const res = await fetch(`${API}/espacios/`, {
        method: "POST",
        headers: {
          "Content-Type":  "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(datos)
      });

      const data = await res.json();

      if (res.ok) {
        mostrarMensaje("mensajeEspacio", "Espacio creado correctamente.", "success");
        formEspacio.reset();
        cargarEspaciosAdmin();
      } else {
        mostrarMensaje("mensajeEspacio", data.detail || "Error al crear espacio.", "error");
      }

    } catch (err) {
      mostrarMensaje("mensajeEspacio", "Error de conexión.", "error");
    }
  });
}

// Cargar datos al iniciar
cargarEspaciosAdmin();
