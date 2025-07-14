// carrito.js: muestra y vacía carrito

document.addEventListener('DOMContentLoaded', () => {
  requireAuth();
  const listEl = document.getElementById('carrito-list');
  const clearBtn = document.getElementById('carrito-clear');

  async function loadCart() {
    const res = await apiFetch('/carrito/carrito/');
    listEl.innerHTML = '';
    let total = 0;
    res.forEach(item => {
      total += item.product.price * item.quantity;
      listEl.innerHTML += `
        <li>
          ${item.product.name} x${item.quantity} — $${item.product.price * item.quantity}
          <button data-id="${item.id}" class="remove-item">X</button>
        </li>
      `;
    });
    document.getElementById('cart-total').textContent = `$${total}`;
    document.querySelectorAll('.remove-item').forEach(btn => {
      btn.onclick = () => {
        apiFetch(`/carrito/carrito/${btn.dataset.id}/`, { method: 'DELETE' })
          .then(loadCart);
      };
    });
  }

  clearBtn.onclick = () => {
    apiFetch('/carrito/carrito/clear/', { method: 'DELETE' })
      .then(loadCart);
  };

  loadCart();
});

document.getElementById('checkout-btn').addEventListener('click', async () => {
  // 1) Creas el pedido contra tu API
  const order = await apiFetch('/pedidos/pedidos/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    // si necesitas enviar algo en body, aquí va
  });
  if (order.id) {
    // 2) Rediriges al pago con su pk
    window.location.href = `/pago/${order.id}/`;
  } else {
    alert('Error al generar el pedido');
  }
});
