const API = "http://localhost:8000";

function getToken() {
  return sessionStorage.getItem("token");
}

function getUsuario() {
  const u = sessionStorage.getItem("usuario");
  return u ? JSON.parse(u) : null;
}

function cerrarSesion() {
  sessionStorage.clear();
  window.location.href = "login.html";
}

function verificarAuth(rolRequerido) {
  const token = getToken();
  const usuario = getUsuario();
  if (!token || !usuario) {
    window.location.href = "login.html";
    return;
  }
  if (rolRequerido && usuario.rol !== rolRequerido) {
    window.location.href = "login.html";
  }
  const nombreEl = document.getElementById("nombreUsuario");
  if (nombreEl) nombreEl.textContent = usuario.nombre;
}

function mostrarTab(nombre) {
  document.querySelectorAll(".tab-content").forEach(t => t.classList.remove("active"));
  document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
  document.getElementById("tab-" + nombre).classList.add("active");
  event.target.classList.add("active");
}

function mostrarMensaje(idElemento, texto, tipo) {
  const el = document.getElementById(idElemento);
  if (!el) return;
  el.textContent = texto;
  el.className = "mensaje " + tipo;
}

// ── Login form ────────────────────────────────────────────────
const loginForm = document.getElementById("loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const correo     = document.getElementById("correo").value.trim();
    const contrasena = document.getElementById("contrasena").value;
    const btnLogin   = document.getElementById("btnLogin");
    const msgError   = document.getElementById("mensajeError");

    btnLogin.textContent = "Ingresando...";
    btnLogin.disabled = true;
    msgError.className = "mensaje error oculto";

    try {
      const res = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ correo, contrasena })
      });

      const data = await res.json();

      if (!res.ok) {
        mostrarMensaje("mensajeError", data.detail || "Error al iniciar sesión.", "error");
        return;
      }

      sessionStorage.setItem("token", data.access_token);
      sessionStorage.setItem("usuario", JSON.stringify({
        id:     data.id_usuario,
        nombre: data.nombre,
        rol:    data.rol
      }));

      if (data.rol === "admin") {
        window.location.href = "dashboard_admin.html";
      } else {
        window.location.href = "dashboard_usuario.html";
      }

    } catch (err) {
      mostrarMensaje("mensajeError", "No se pudo conectar con el servidor.", "error");
    } finally {
      btnLogin.textContent = "Ingresar";
      btnLogin.disabled = false;
    }
  });
}
