// app.js: utilidades globales

const API_BASE = window.location.origin + '/api';

function getToken() {
  return localStorage.getItem('token');
}

function apiFetch(path, opts = {}) {
  const headers = opts.headers || {};
  const token = getToken();
  if (token) headers['Authorization'] = 'Bearer ' + token;
  opts.headers = { 'Content-Type': 'application/json', ...headers };
  return fetch(API_BASE + path, opts).then(r => r.json());
}

// Redirigir si no está autenticado
function requireAuth() {
  if (!getToken()) window.location.href = '/login/';
}

// Al cargar cualquier página
document.addEventListener('DOMContentLoaded', () => {
  // Aquí podrías comprobar rol, mostrar/ocultar botones, etc.
});