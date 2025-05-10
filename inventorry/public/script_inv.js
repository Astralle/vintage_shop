// public/script_inv.js

// We'll store the key here once unlocked
let API_KEY = null;

// Base API URL
const apiUrl = '/api/items';

// Helper to get auth headers
function getAuthHeaders() {
  return {
    'Content-Type': 'application/json',
    'X-API-KEY': API_KEY
  };
}

// Fetch list of items (no auth needed)
async function fetchItems() {
  const res = await fetch(apiUrl);
  if (!res.ok) throw new Error('Échec du chargement des éléments');
  return res.json();
}

// Render the list into the <ul id="item-list">
function renderList(items) {
  const ul = document.getElementById('item-list');
  ul.innerHTML = '';
  items.forEach(item => {
    const li = document.createElement('li');
    li.innerHTML = `
      <strong>${item.name}</strong> — ${item.price}€
      <button data-id="${item.id}" class="edit-btn" ${API_KEY ? '' : 'disabled'}>✏️</button>
      <button data-id="${item.id}" class="del-btn"  ${API_KEY ? '' : 'disabled'}>🗑️</button>
    `;
    ul.appendChild(li);
  });
}

// Fill the form fields for editing
function fillForm(item) {
  document.getElementById('item-id').value          = item.id;
  document.getElementById('name').value             = item.name || '';
  document.getElementById('price').value            = item.price || '';
  document.getElementById('shortDescription').value = item.shortDescription || '';
  document.getElementById('longDescription').value  = item.longDescription || '';
  document.getElementById('tags').value             = (item.tags || []).join(',');
  document.getElementById('form-title').textContent = 'Modifier un produit';
  document.getElementById('cancel-btn').style.display = 'inline';
}

// Reset the form to “add” mode
function resetForm() {
  document.getElementById('item-form').reset();
  document.getElementById('item-id').value = '';
  document.getElementById('form-title').textContent = 'Ajouter un produit';
  document.getElementById('cancel-btn').style.display = 'none';
}

// Handle form submission for create & update
document.getElementById('item-form').addEventListener('submit', async e => {
  e.preventDefault();
  if (!API_KEY) return alert('Vous devez d’abord déverrouiller avec le mot de passe.');

  const id = document.getElementById('item-id').value;
  const data = {
    name: document.getElementById('name').value,
    price: parseFloat(document.getElementById('price').value),
    shortDescription: document.getElementById('shortDescription').value,
    longDescription: document.getElementById('longDescription').value,
    tags: document.getElementById('tags')
            .value
            .split(',')
            .map(t => t.trim())
            .filter(t => t)
  };

  try {
    let res;
    if (id) {
      // Update existing
      res = await fetch(`${apiUrl}/${id}`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify(data)
      });
    } else {
      // Create new
      res = await fetch(apiUrl, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(data)
      });
    }

    if (res.status === 401) {
      alert('Mot de passe invalide');
      return;
    }
    if (!res.ok) {
      alert('Erreur serveur');
      return;
    }

    resetForm();
    loadAndRender();
  } catch (err) {
    console.error(err);
    alert('Erreur de connexion au serveur');
  }
});

// Cancel edit
document.getElementById('cancel-btn').addEventListener('click', resetForm);

// Delegate edit/delete button clicks
document.getElementById('item-list').addEventListener('click', async e => {
  const id = e.target.dataset.id;
  if (e.target.classList.contains('edit-btn')) {
    if (!API_KEY) return alert('Déverrouillez d’abord avec le mot de passe.');
    const items = await fetchItems();
    const item = items.find(i => i.id == id);
    fillForm(item);
  }
  if (e.target.classList.contains('del-btn')) {
    if (!API_KEY) return alert('Déverrouillez d’abord avec le mot de passe.');
    if (!confirm('Supprimer cet item ?')) return;
    try {
      const res = await fetch(`${apiUrl}/${id}`, {
        method: 'DELETE',
        headers: getAuthHeaders()
      });
      if (res.status === 401) {
        alert('Mot de passe invalide');
        return;
      }
      if (!res.ok) {
        alert('Erreur lors de la suppression');
        return;
      }
      loadAndRender();
    } catch (err) {
      console.error(err);
      alert('Erreur de connexion');
    }
  }
});

// Unlock button—reads the password field into our API_KEY
document.getElementById('unlock-btn').addEventListener('click', () => {
  const key = document.getElementById('api-key').value.trim();
  if (!key) return alert('Entrez un mot de passe.');
  API_KEY = key;
  document.getElementById('api-key').value = '';
  // re-render so edit/delete buttons become enabled
  loadAndRender();
});

// Initial load (read-only)
async function loadAndRender() {
  try {
    const items = await fetchItems();
    renderList(items);
  } catch (err) {
    console.error(err);
    alert('Impossible de charger la liste');
  }
}

// First render
loadAndRender();
