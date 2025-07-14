// pedidos.js: genera y lista pedidos

document.addEventListener('DOMContentLoaded', () => {
  requireAuth();
  const form = document.getElementById('order-form');
  const listEl = document.getElementById('orders-list');

  async function loadOrders() {
    const res = await apiFetch('/pedidos/pedidos/');
    listEl.innerHTML = '';
    res.forEach(o => {
      listEl.innerHTML += `<li>Pedido #${o.id} — ${o.status} — $${o.total}</li>`;
    });
  }

  form?.addEventListener('submit', async e => {
    e.preventDefault();
    const res = await apiFetch('/pedidos/pedidos/', { method: 'POST' });
    if (res.id) {
      alert('Pedido creado: #' + res.id);
      window.location.href = `/pago/${res.id}/`;
    }
  });

  loadOrders();
});