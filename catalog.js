fetch('items.json')
  .then(response => response.json())
  .then(items => {
    const grid = document.getElementById('catalog-grid');
    items.forEach(item => {
      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = `
        <a href="product.html?id=${item.id}">
          <img src="${item.image}" alt="${item.name}">
          <h3>${item.name}</h3>
          <p>${item.description}</p>
        </a>
      `;
      grid.appendChild(card);
    });
  })
  .catch(error => {
    document.getElementById('catalog-grid').innerHTML = "<p>Erreur de chargement du catalogue.</p>";
    console.error("Erreur:", error);
  });
