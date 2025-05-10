document.addEventListener('DOMContentLoaded', async () => {
  // Grab existing sections
  const filtersSection = document.querySelector('.shop-filters');
  const shopGrid       = document.querySelector('.shop-grid');
  let products         = [];
  let activeTag        = '';
  let searchText       = '';

  // Make filtersSection a flex container for spacing
  filtersSection.style.display = 'flex';
  filtersSection.style.alignItems = 'center';
  filtersSection.style.justifyContent = 'space-between';

  // 1) Inject filter-buttons container
  const filtersContainer = document.createElement('div');
  filtersContainer.id = 'filter-buttons';
  // Flex layout and gap between buttons
  filtersContainer.style.display = 'flex';
  filtersContainer.style.flexWrap = 'wrap';
  filtersContainer.style.gap = '12px';
  // Let filter buttons container grow to fill space
  filtersContainer.style.flexGrow = '1';
  filtersContainer.style.marginRight = '16px';
  filtersSection.appendChild(filtersContainer);

  // 2) Inject search wrapper
  const searchWrapper = document.createElement('div');
  searchWrapper.classList.add('search-wrapper');
  const searchInput   = document.createElement('input');
  searchInput.id           = 'search-input';
  searchInput.type         = 'text';
  searchInput.placeholder  = 'Que cherchez-vous ?';
  const searchButton      = document.createElement('button');
  searchButton.id          = 'search-button';
  searchButton.type        = 'button';
  searchButton.innerHTML   = '&#128269;';
  searchWrapper.append(searchInput, searchButton);
  filtersSection.appendChild(searchWrapper);

  try {
    const res = await fetch('/api/products');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    products = await res.json();
    if (!Array.isArray(products)) throw new Error('Format data invalide');

    // Count occurrences of each tag
    const tagCounts = products
      .flatMap(p => p.tags)
      .reduce((acc, tag) => {
        acc[tag] = (acc[tag] || 0) + 1;
        return acc;
      }, {});

    // Select only the 6 most frequent tags
    const tags = Object.entries(tagCounts)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 6)
      .map(([tag]) => tag);

    // "Tout" button
    const allBtn = document.createElement('button');
    allBtn.textContent        = 'Tout';
    allBtn.classList.add('category-btn', 'active');
    allBtn.dataset.tag        = '';
    filtersContainer.appendChild(allBtn);

    // Buttons for top-6 tags
    tags.forEach(tag => {
      const btn = document.createElement('button');
      btn.textContent          = tag.charAt(0).toUpperCase() + tag.slice(1);
      btn.classList.add('category-btn');
      btn.dataset.tag          = tag;
      filtersContainer.appendChild(btn);
    });

    // Tag filter clicks
    filtersContainer.addEventListener('click', e => {
      if (!e.target.matches('.category-btn')) return;
      filtersContainer
        .querySelectorAll('.category-btn')
        .forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      activeTag = e.target.dataset.tag;
      renderProducts();
    });

    // Search interactions
    searchInput.addEventListener('input', e => {
      searchText = e.target.value.trim().toLowerCase();
      renderProducts();
    });
    searchButton.addEventListener('click', renderProducts);

    // Initial display
    renderProducts();

  } catch (err) {
    console.error('[Boutique] Erreur:', err);
    shopGrid.innerHTML = `<p>Impossible de charger les produits : ${err.message}</p>`;
  }

  // Render function: filters by tag + text
  function renderProducts() {
    shopGrid.innerHTML = '';
    products.forEach(p => {
      const matchTag = !activeTag || p.tags.includes(activeTag);
      const inSearch = !searchText || [
        p.name,
        p.shortDescription,
        p.longDescription,
        ...p.tags
      ].some(field => field.toLowerCase().includes(searchText));

      if (matchTag && inSearch) {
        const card = document.createElement('div');
        card.classList.add('product-card');
        card.innerHTML = `
          <a href="/product/${p.id}">
            <div class="product-image">
              <img src="../static/${p.coverImage}" alt="${p.name}">
            </div>
            <div class="product-info">
              <h3>${p.name}</h3>
              <p class="price">${p.price} €</p>
              <p>${p.shortDescription}</p>
            </div>
          </a>
        `;
        shopGrid.appendChild(card);
      }
    });
  }
});
