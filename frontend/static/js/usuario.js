document.addEventListener('DOMContentLoaded', () => {
  const loginForm    = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');
  const authLinks    = document.getElementById('auth-links');
  const userMenu     = document.getElementById('user-menu');
  const navUsername  = document.getElementById('nav-username');
  const userDropdown = document.getElementById('user-dropdown');
  const navLogout    = document.getElementById('nav-logout');

  // Función genérica para llamadas API con token
  async function apiFetch(path, opts = {}) {
    opts.headers = opts.headers || {};
    opts.headers['Content-Type'] = 'application/json';
    const token = localStorage.getItem('token');
    if (token) opts.headers['Authorization'] = 'Token ' + token;
    const resp = await fetch(window.baseUrl + '/api' + path, opts);
    return resp.json();
  }

  // --- LOGIN ---
  if (loginForm) {
    loginForm.addEventListener('submit', async e => {
      e.preventDefault();
      const username = document.getElementById('login-usuario').value;
      const password = document.getElementById('login-password').value;
      const res = await apiFetch('/usuarios/login/', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
      });
      if (res.token) {
        localStorage.setItem('token', res.token);
        localStorage.setItem('username', res.user.username);
        localStorage.setItem('role', res.user.role);
        window.location.href = '/';
      } else {
        alert(res.detail || 'Error al iniciar sesión');
      }
    });
  }

  // --- REGISTRO ---
  if (registerForm) {
    registerForm.addEventListener('submit', async e => {
      e.preventDefault();
      const email    = document.getElementById('register-email').value;
      const username = document.getElementById('register-username').value;
      const password = document.getElementById('register-password').value;
      const res = await apiFetch('/usuarios/register/', {
        method: 'POST',
        body: JSON.stringify({ email, username, password }),
      });
      if (res.token) {
        localStorage.setItem('token', res.token);
        localStorage.setItem('username', res.user.username);
        localStorage.setItem('role', res.user.role);
        window.location.href = '/';
      } else {
        alert(res.detail || 'Error al registrarse');
      }
    });
  }

  // --- CONTROL DE NAVBAR según estado de auth y rol ---
  function updateNavbar() {
    const token    = localStorage.getItem('token');
    const username = localStorage.getItem('username');
    const role     = localStorage.getItem('role');

    // Mostrar u ocultar auth links vs user menu
    if (token && username && role) {
      authLinks.style.display = 'none';
      userMenu.style.display  = 'inline-block';
      navUsername.textContent = username;

      // Adaptar enlaces según rol
      // Cliente
      document.getElementById('nav-carrito').style.display =
        role === 'cliente' ? 'inline-block' : 'none';
      document.getElementById('nav-pedidos').style.display =
        role === 'cliente' ? 'inline-block' : 'none';

      // Vendedor
      const vendDash = document.getElementById('nav-dashboard-vendedor');
      if (vendDash) {
        vendDash.style.display = role === 'vendedor' ? 'inline-block' : 'none';
      }

      // Bodeguero
      const bodDash = document.getElementById('nav-dashboard-bodeguero');
      if (bodDash) {
        bodDash.style.display = role === 'bodeguero' ? 'inline-block' : 'none';
      }

      // Contador
      const contDash = document.getElementById('nav-dashboard-contador');
      if (contDash) {
        contDash.style.display = role === 'contador' ? 'inline-block' : 'none';
      }

      // Administrador
      const adminDash = document.getElementById('nav-dashboard-admin');
      if (adminDash) {
        adminDash.style.display =
          role === 'administrador' ? 'inline-block' : 'none';
      }

    } else {
      // Sin sesión
      authLinks.style.display = 'inline-block';
      userMenu.style.display  = 'none';

      // Ocultar todos los enlaces de roles
      ['nav-carrito','nav-pedidos',
       'nav-dashboard-vendedor','nav-dashboard-bodeguero',
       'nav-dashboard-contador','nav-dashboard-admin'
      ].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.style.display = 'none';
      });
    }
  }
  updateNavbar();

  // --- TOGGLE DROPDOWN ---
  navUsername && navUsername.addEventListener('click', () => {
    userDropdown.style.display =
      userDropdown.style.display === 'none' ? 'block' : 'none';
  });

  // --- LOGOUT ---
  navLogout && navLogout.addEventListener('click', () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    localStorage.removeItem('role');
    window.location.href = '/';
  });
});