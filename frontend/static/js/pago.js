// pago.js: mock de Transbank

document.addEventListener('DOMContentLoaded', () => {
  requireAuth();
  const initBtn = document.getElementById('pay-init');
  const confirmBtn = document.getElementById('pay-confirm');
  const statusEl = document.getElementById('pay-status');

  initBtn?.addEventListener('click', async () => {
    const orderId = initBtn.dataset.orderId;
    const res = await apiFetch('/pagos/initiate/', {
      method: 'POST',
      body: JSON.stringify({ order_id: orderId }),
    });
    window.location.href = res.url;
  });

  confirmBtn?.addEventListener('click', async () => {
    const token = confirmBtn.dataset.token;
    const res = await apiFetch('/pagos/confirm/', {
      method: 'POST',
      body: JSON.stringify({ token }),
    });
    statusEl.textContent = res.status;
  });
});