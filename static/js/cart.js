// Shared cart count updater for all pages
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('cart-count')) {
        const cart = JSON.parse(localStorage.getItem(`cart_${CURRENT_USER}`) || '[]');
        const count = cart.reduce((acc, item) => acc + item.qty, 0);
        document.getElementById('cart-count').innerText = count;
    }
});