document.addEventListener('DOMContentLoaded', async () => {
  // Extract the product ID from the URL path (/product/123)
  const segments = window.location.pathname.split('/').filter(seg => seg);
  const id = parseInt(segments[segments.length - 1], 10);

  if (isNaN(id)) {
    console.error('[Produit] ID invalide dans l\'URL:', window.location.pathname);
    return;
  }

  try {
    // Choose endpoint based on ID sign
    const endpoint = id > 0 ? '/api/products' : '/api/featured';
    const response = await fetch(endpoint);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    if (!Array.isArray(data)) {
      throw new Error('Le JSON retourné n’est pas un tableau');
    }

    // Find matching product
    const p = data.find(item => item.id === id);
    const container = document.getElementById('product-container');
    if (!container) {
      console.error('[Produit] #product-container introuvable');
      return;
    }

    if (!p) {
      container.innerHTML = '<p>Produit non trouvé.</p>';
      console.warn(`[Produit] Aucun produit avec id=${id} in ${endpoint}`);
      return;
    }

    // Prefix static paths for images
    const coverSrc = `/static/${p.coverImage}`;
    const detailSrcs = p.detailImages.map(img => `/static/${img}`);

    // Render product details
    container.innerHTML = `
      <div class="product-images">
        <img class="cover" src="${coverSrc}" alt="${p.name}">
        <div class="details">
          ${detailSrcs.map(src => `<img src="${src}" alt="${p.name} détail">`).join('')}
        </div>
      </div>
      <div class="product-info">
        <h1>${p.name}</h1>
        <p class="price">${p.price} €</p>
        <p>${p.longDescription}</p>
        <div class="tags">
          ${p.tags.map(tag => `<span>${tag}</span>`).join('')}
        </div>
        <button id="reserve-btn">Réserver</button>
      </div>
    `;

    // Swap cover on thumbnail hover/click
    const coverImg = container.querySelector('.product-images .cover');
    const thumbImgs = container.querySelectorAll('.product-images .details img');
    thumbImgs.forEach(thumb => {
      thumb.addEventListener('mouseover', () => coverImg.src = thumb.src);
      thumb.addEventListener('click', () => coverImg.src = thumb.src);
    });

    // Reservation handler
    document.getElementById('reserve-btn').addEventListener('click', () => {
      alert(`Vous avez réservé : ${p.name}`);
    });

    console.log(`[Produit] Détails affichés pour id=${id} from ${endpoint}`);

  } catch (err) {
    console.error('[Produit] Erreur chargement produit :', err);
    const container = document.getElementById('product-container');
    if (container) container.innerHTML = '<p>Impossible de charger le produit.</p>';
  }
});