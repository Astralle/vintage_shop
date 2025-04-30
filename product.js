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
        <img src="\${product.image}" alt="\${product.name}" style="width: 300px; max-width: 100%; border-radius: 8px; margin-bottom: 20px;">
        <p>\${product.description}</p>
        <button onclick="addToCart(\${product.id})" style="padding: 10px 20px; margin-top: 20px; background-color: #FFD700; color: black; border: none; border-radius: 5px; cursor: pointer;">
          Ajouter au panier
        </button>
      `;
    } else {
      container.innerHTML = "<p>Produit non trouvé.</p>";
    }
  })
  .catch(error => {
    document.getElementById("product-detail").innerHTML = "<p>Erreur de chargement du produit.</p>";
    console.error("Erreur:", error);
  });

function addToCart(productId) {
  let cart = JSON.parse(localStorage.getItem("cart")) || [];
  cart.push(productId);
  localStorage.setItem("cart", JSON.stringify(cart));
  alert("Produit ajouté au panier !");
}
