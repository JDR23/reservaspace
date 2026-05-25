async function cargarEspacios() {
  const token = getToken();
  const contenedor = document.getElementById("listaEspacios");
  contenedor.innerHTML = "<p>Cargando...</p>";

  try {
    const res = await fetch(`${API}/espacios/activos`, {
      headers: { "Authorization": `Bearer ${token}` }
    });
    const espacios = await res.json();

    if (!espacios.length) {
      contenedor.innerHTML = "<p>No hay espacios disponibles.</p>";
      return;
    }

    contenedor.innerHTML = espacios.map(e => `
      <div class="card">
        <h3>🏢 ${e.nombre}</h3>
        <p>📍 ${e.ubicacion}</p>
        <p>👥 Capacidad: ${e.capacidad} personas</p>
        <p>Estado: <span class="estado-${e.estado}">${e.estado}</span></p>
      </div>
    `).join("");

    // Llenar select de reservas
    const select = document.getElementById("id_espacio");
    if (select) {
      select.innerHTML = espacios.map(e =>
        `<option value="${e.id_espacio}">${e.nombre} (cap. ${e.capacidad})</option>`
      ).join("");
    }

  } catch (err) {
    contenedor.innerHTML = "<p>Error al cargar espacios.</p>";
  }
}

// Cargar espacios automáticamente si estamos en el dashboard usuario
if (document.getElementById("listaEspacios")) {
  verificarAuth("usuario");
  cargarEspacios();
}
