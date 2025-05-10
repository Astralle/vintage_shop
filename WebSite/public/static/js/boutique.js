document.addEventListener('DOMContentLoaded', async () => {
  const shopGrid = document.getElementById('shop-grid');
  if (!shopGrid) {
    console.error('[Boutique] #shop-grid introuvable dans le DOM');
    return;
  }

  try {
    // Fetch products from secured API
    const response = await fetch('/api/products');
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
      shopGrid.innerHTML = ''; // reset
      products.forEach(p => {
        const card = document.createElement('div');
        card.className = 'product-card';
        // Prefix static path for cover image
        const coverSrc = `/static/${p.coverImage}`;
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
      console.log(`[Boutique] ${products.length} produits affichés`);
    }

  } catch (err) {
    console.error('[Boutique] Erreur chargement produits :', err);
    shopGrid.innerHTML = `<p>Impossible de charger les produits : ${err.message}</p>`;
  }
});
