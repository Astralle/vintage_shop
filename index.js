fetch('products.json')
    .then(response => response.json())
    .then(data => {
      const container = document.getElementById('card-container');
      data.forEach(product => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
          <img src="${product.image}" alt="${product.alt}">
          <p>${product.description}</p>
          <a><button>Voir le produit</button></a>
        `;
        container.appendChild(card);
      });
    })
    .catch(error => console.error('Erreur lors du chargement des produits:', error));