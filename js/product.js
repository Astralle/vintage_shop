document.addEventListener('DOMContentLoaded', () => {
  // Récupère l’ID depuis l’URL (?id=)
  const params = new URLSearchParams(window.location.search);
  const id = parseInt(params.get('id'), 10);

  // Détermine le fichier JSON à charger
  const jsonPath = id > 0 ? './products.json' : './featured.json';  // Si l'ID est positif, charge products.json, sinon featured.json
  console.log('📦 [Produit] fetch vers :', jsonPath);

  fetch(jsonPath)
    .then(res => {
      console.log('📡 [Produit] statut fetch:', res.status, res.url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    })
    .then(data => {
      const container = document.getElementById('product-container');
      if (!container) {
        console.error('❌ [Produit] #product-container introuvable');
        return;
      }

      // Récupère le produit correspondant à l'ID
      const p = data.find(item => item.id === id);

      if (!p) {
        container.innerHTML = '<p>Produit non trouvé.</p>';
        console.warn(`⚠️ [Produit] Aucun produit avec id=${id}`);
        return;
      }

      // Affichage des images et infos
      container.innerHTML = `
        <div class="product-images">
          <img class="cover" src="${p.coverImage}" alt="${p.name}">
          <div class="details">
            ${p.detailImages.map(img => `<img src="${img}" alt="${p.name} détail">`).join('')}
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

      // Swap cover on thumbnail hover or click
      const coverImg = container.querySelector('.product-images .cover');
      const thumbImgs = container.querySelectorAll('.product-images .details img');
      thumbImgs.forEach(thumb => {
        thumb.addEventListener('mouseover', () => {
          coverImg.src = thumb.src;
        });
        thumb.addEventListener('click', () => {
          coverImg.src = thumb.src;
        });
      });

      // Réservation
      document.getElementById('reserve-btn').addEventListener('click', () => {
        alert(`Vous avez réservé : ${p.name}`);
      });

      console.log(`✅ [Produit] Détails affichés pour id=${id}`);
    })
    .catch(err => {
      console.error('🔥 [Produit] Erreur chargement produit :', err);
      const container = document.getElementById('product-container');
      if (container) container.innerHTML = '<p>Impossible de charger le produit.</p>';
    });
});
