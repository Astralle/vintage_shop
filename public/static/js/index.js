document.addEventListener('DOMContentLoaded', async () => {
  const shopGrid = document.getElementById('shop-grid');
  if (!shopGrid) {
    console.error('[Index] #shop-grid introuvable dans le DOM');
    return;
  }

  try {
    // Fetch all products from secured API
    const response = await fetch('/api/products');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const products = await response.json();
    if (!Array.isArray(products)) {
      throw new Error('Le JSON retourné n’est pas un tableau');
    }

    // Only positive IDs and limit to first 4 items
    const positiveProducts = products.filter(p => p.id > 0);
    const limitedProducts = positiveProducts.slice(0, 3);

    if (limitedProducts.length === 0) {
      shopGrid.innerHTML = '<p>Aucun produit disponible.</p>';
    } else {
      shopGrid.innerHTML = '';
      limitedProducts.forEach(p => {
        // Prefix static path for cover image
        const coverSrc = `/static/${p.coverImage}`;
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
          <a href="/product/${p.id}">
            <img src="${coverSrc}" alt="${p.name}">
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
    shopGrid.innerHTML = `<p>Impossible de charger les produits : ${err.message}</p>`;
  }
});
