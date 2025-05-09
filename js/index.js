document.addEventListener('DOMContentLoaded', async () => {
  const shopGrid = document.getElementById('shop-grid'); // Ensure this container exists in HTML
  if (!shopGrid) {
    console.error('[Index] #shop-grid introuvable dans le DOM');
    return;
  }

  try {
    const response = await fetch('featured.json');  // Fetch data from featured.json
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const products = await response.json();
    if (!Array.isArray(products)) {
      throw new Error('Le JSON retourné n’est pas un tableau');
    }

    if (products.length === 0) {
      shopGrid.innerHTML = '<p>Aucun produit disponible.</p>';
    } else {
      shopGrid.innerHTML = ''; // Clear the grid
      const limitedProducts = products.slice(0, 6); // Limit to 6 products
      limitedProducts.forEach(p => {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
          <a href="product.html?id=${p.id}">
            <img src="${p.coverImage}" alt="${p.name}">
            <div class="info">
              <h3>${p.name}</h3>
              <p class="price">${p.price} €</p>
              <p>${p.shortDescription}</p>
            </div>
          </a>
        `;
        shopGrid.appendChild(card);
      });
      console.log(`[Index] ${limitedProducts.length} produits affichés`);
    }

  } catch (err) {
    console.error('[Index] Erreur chargement produits :', err);
    shopGrid.innerHTML = `<p>Impossible de charger les produits : ${err.message}</p>`;
  }
});
