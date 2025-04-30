function getQueryParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
}

const productId = getQueryParam("id");

fetch('items.json')
  .then(response => response.json())
  .then(items => {
    const product = items.find(item => item.id == productId);
    const container = document.getElementById("product-detail");

    if (product) {
      container.innerHTML = `
        <h2>${product.name}</h2>
        <img src="${product.image}" alt="${product.name}" style="width: 300px; max-width: 100%; border-radius: 8px; margin-bottom: 20px;">
        <p>${product.description}</p>
      `;
    } else {
      container.innerHTML = "<p>Produit non trouvé.</p>";
    }
  })
  .catch(error => {
    document.getElementById("product-detail").innerHTML = "<p>Erreur de chargement du produit.</p>";
    console.error("Erreur:", error);
  });
