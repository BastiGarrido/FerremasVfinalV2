// catalogo.js: carga y filtra productos

document.addEventListener('DOMContentLoaded', () => {
  const grid = document.getElementById('catalogo-grid');
  const countCurr = document.getElementById('count-current');
  const countTotal = document.getElementById('count-total');
  const orderSel = document.getElementById('order-select');
  const catSel   = document.getElementById('category-select');
  const minInput = document.getElementById('price-min');
  const maxInput = document.getElementById('price-max');
  const applyBtn = document.getElementById('filter-apply');

  let allCats = new Set();

  async function load() {
    const params = new URLSearchParams();
    if (orderSel.value) params.append('ordering', orderSel.value);
    if (catSel.value)   params.append('category', catSel.value);
    if (minInput.value) params.append('price_min', minInput.value);
    if (maxInput.value) params.append('price_max', maxInput.value);

    const res = await apiFetch('/productos/productos/?' + params.toString());
    grid.innerHTML = '';
    res.results.forEach(p => {
      allCats.add(p.category);
      const card = document.createElement('div');
      card.className = 'product-card';
      card.innerHTML = `
        <img src="${p.image_url}" alt="${p.name}">
        <h3>${p.name}</h3>
        <div class="price">$${p.price}</div>
        <button data-id="${p.id}">Agregar</button>
      `;
      grid.append(card);
      card.querySelector('button').onclick = () => {
        if (!getToken()) return requireAuth();
        apiFetch('/carrito/carrito/', {
          method: 'POST',
          body: JSON.stringify({ product: p.id, quantity: 1 }),
        }).then(() => alert('Añadido al carrito'));
      };
    });
    countCurr.textContent = res.results.length;
    countTotal.textContent = res.count;

    // Poblamos categorías
    catSel.innerHTML = '<option value=\"\">Todas</option>';
    Array.from(allCats).forEach(c => {
      catSel.insertAdjacentHTML('beforeend', `<option value="${c}">${c}</option>`);
    });
  }

  applyBtn.addEventListener('click', load);
  load();
});