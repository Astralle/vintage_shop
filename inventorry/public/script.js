const apiUrl = '/api/items';

async function fetchItems() {
  const res = await fetch(apiUrl);
  return res.json();
}

function renderList(items) {
  const ul = document.getElementById('item-list');
  ul.innerHTML = '';
  items.forEach(item => {
    const li = document.createElement('li');
    li.innerHTML = `
      <strong>${item.name}</strong> — ${item.price}€
      <button data-id="${item.id}" class="edit-btn">✏️</button>
      <button data-id="${item.id}" class="del-btn">🗑️</button>
    `;
    ul.appendChild(li);
  });
}

function fillForm(item) {
  document.getElementById('item-id').value         = item.id;
  document.getElementById('name').value            = item.name || '';
  document.getElementById('price').value           = item.price || '';
  document.getElementById('shortDescription').value= item.shortDescription || '';
  document.getElementById('longDescription').value = item.longDescription || '';
  document.getElementById('tags').value            = (item.tags||[]).join(',');
  document.getElementById('form-title').textContent= 'Modifier un produit';
  document.getElementById('cancel-btn').style.display = 'inline';
}

function resetForm() {
  document.getElementById('item-form').reset();
  document.getElementById('item-id').value = '';
  document.getElementById('form-title').textContent = 'Ajouter un produit';
  document.getElementById('cancel-btn').style.display = 'none';
}

document.getElementById('item-form').addEventListener('submit', async e => {
  e.preventDefault();
  const id   = document.getElementById('item-id').value;
  const data = {
    name: document.getElementById('name').value,
    price: parseFloat(document.getElementById('price').value),
    shortDescription: document.getElementById('shortDescription').value,
    longDescription: document.getElementById('longDescription').value,
    tags: document.getElementById('tags').value.split(',').map(t=>t.trim()).filter(t=>t)
  };

  if (id) {
    // update
    await fetch(`${apiUrl}/${id}`, {
      method: 'PUT',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(data)
    });
  } else {
    // create
    await fetch(apiUrl, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(data)
    });
  }
  resetForm();
  loadAndRender();
});

document.getElementById('cancel-btn').addEventListener('click', resetForm);

document.getElementById('item-list').addEventListener('click', async e => {
  const id = e.target.dataset.id;
  if (e.target.classList.contains('edit-btn')) {
    const items = await fetchItems();
    const item  = items.find(i=>i.id==id);
    fillForm(item);
  }
  if (e.target.classList.contains('del-btn')) {
    if (confirm('Supprimer cet item ?')) {
      await fetch(`${apiUrl}/${id}`, { method: 'DELETE' });
      loadAndRender();
    }
  }
});

async function loadAndRender() {
  const items = await fetchItems();
  renderList(items);
}
loadAndRender();
