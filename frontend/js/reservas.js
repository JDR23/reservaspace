async function cargarMisReservas() {
  const token = getToken();
  const contenedor = document.getElementById("listaMisReservas");
  contenedor.innerHTML = "<p>Cargando...</p>";

  try {
    const res = await fetch(`${API}/reservas/mis-reservas`, {
      headers: { "Authorization": `Bearer ${token}` }
    });
    const reservas = await res.json();

    if (!reservas.length) {
      contenedor.innerHTML = "<p>No tienes reservas registradas.</p>";
      return;
    }

    contenedor.innerHTML = reservas.map(r => `
      <div class="card">
        <h3>📅 Reserva #${r.id_reserva}</h3>
        <p>🏢 Espacio ID: ${r.id_espacio}</p>
        <p>📆 Fecha: ${r.fecha}</p>
        <p>🕐 Horario: ${r.hora_inicio} - ${r.hora_fin}</p>
        <p>👥 Asistentes: ${r.cantidad_asistentes}</p>
        <p>Estado: <span class="estado-${r.estado}">${r.estado}</span></p>
        <div class="card-actions">
          ${r.estado === "esperando" ? `
            <button class="btn-danger" onclick="cancelarReserva(${r.id_reserva})">
              Cancelar
            </button>` : ""}
        </div>
      </div>
    `).join("");

  } catch (err) {
    contenedor.innerHTML = "<p>Error al cargar reservas.</p>";
  }
}

async function cancelarReserva(id) {
  if (!confirm("¿Deseas cancelar esta reserva?")) return;
  const token = getToken();

  try {
    const res = await fetch(`${API}/reservas/${id}`, {
      method: "DELETE",
      headers: { "Authorization": `Bearer ${token}` }
    });

    if (res.ok) {
      alert("Reserva cancelada correctamente.");
      cargarMisReservas();
    } else {
      const data = await res.json();
      alert("Error: " + (data.detail || "No se pudo cancelar."));
    }
  } catch (err) {
    alert("Error de conexión.");
  }
}

// Formulario de nueva reserva
const formReserva = document.getElementById("formReserva");
if (formReserva) {
  formReserva.addEventListener("submit", async (e) => {
    e.preventDefault();
    const token = getToken();

    const datos = {
      id_espacio:          parseInt(document.getElementById("id_espacio").value),
      fecha:               document.getElementById("fecha").value,
      hora_inicio:         document.getElementById("hora_inicio").value + ":00",
      hora_fin:            document.getElementById("hora_fin").value + ":00",
      cantidad_asistentes: parseInt(document.getElementById("cantidad_asistentes").value)
    };

    try {
      const res = await fetch(`${API}/reservas/`, {
        method: "POST",
        headers: {
          "Content-Type":  "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(datos)
      });

      const data = await res.json();

      if (res.ok) {
        mostrarMensaje("mensajeReserva", "Reserva creada correctamente. Estado: esperando aprobación.", "success");
        formReserva.reset();
        cargarEspacios();
      } else {
        mostrarMensaje("mensajeReserva", data.detail || "Error al crear la reserva.", "error");
      }

    } catch (err) {
      mostrarMensaje("mensajeReserva", "Error de conexión con el servidor.", "error");
    }
  });
}
