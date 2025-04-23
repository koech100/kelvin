const pages = ['home', 'products', 'cart', 'about'];
const cart = [];

// Show specific section
function show(page) {
  pages.forEach(p => {
    const section = document.getElementById(p);
    if (section) section.classList.add('hidden');
  });
  const pageElement = document.getElementById(page);
  if (pageElement) pageElement.classList.remove('hidden');
}

// Add product and disable button
function addToCart(name, price, button) {
  const existing = cart.find(item => item.name === name);
  if (!existing) {
    cart.push({ name, price });
    button.disabled = true;
    button.textContent = "✔️ Added";
    updateCart();
  }
}

// Remove product
function removeFromCart(name) {
  const index = cart.findIndex(item => item.name === name);
  if (index > -1) {
    cart.splice(index, 1);
    updateCart();
    // Re-enable button
    const buttons = document.querySelectorAll(`.product button`);
    buttons.forEach(btn => {
      if (btn.previousElementSibling && btn.previousElementSibling.textContent.trim() === name) {
        btn.disabled = false;
        btn.textContent = "Add to Cart";
      }
    });
  }
}

// Update cart display
function updateCart() {
  const itemsDiv = document.getElementById('cart-items');
  const totalEl = document.getElementById('cart-total');

  itemsDiv.innerHTML = '';
  let total = 0;

  if (cart.length === 0) {
    itemsDiv.innerHTML = "<p>Your cart is empty. Add some products to proceed.</p>";
  }

  cart.forEach(item => {
    total += item.price;
    const div = document.createElement('div');
    div.className = 'cart-item';
    div.innerHTML = `
      ${item.name} - $${item.price}
      <button class="remove-btn" onclick="removeFromCart('${item.name}')">🗑️ Remove</button>
    `;
    itemsDiv.appendChild(div);
  });

  totalEl.innerHTML = `<strong>Total:</strong> $${total.toFixed(2)}`;
}

// Function to email cart items
function emailCartItems() {
  if (cart.length === 0) {
    alert("Your cart is empty!");
    return;
  }

  // Prepare the email content
  let emailBody = "Here are the items in my cart:\n\n";
  cart.forEach(item => {
    emailBody += `${item.name} - $${item.price}\n`;
  });

  // Encode the email subject and body to make it URL-friendly
  const subject = encodeURIComponent('Cart Items');
  const body = encodeURIComponent(emailBody);
  
  // Open the user's email client with a pre-filled email
  window.location.href = `mailto:young111doodle@gmail.com?subject=${subject}&body=${body}`;
}

// Footer year
document.getElementById('year').textContent = new Date().getFullYear();

