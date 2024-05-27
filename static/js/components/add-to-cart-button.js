import { LocalStorageService } from "../services/local-storage.service.js";

class AddToCartButton extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        const button = document.createElement('button');
        button.textContent = 'Agregar al carrito';
        const style = document.createElement('style');
        style.textContent = `
            button {
                background-color: #4CAF50;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border: none;
                border-radius: 4px;
            }
        `;
        this.shadowRoot.append(style, button);
        this.productSKU = this.getAttribute('product-sku');
        button.addEventListener('click', () => {
            this.addToCart();
        });
    }

    addToCart() {
        const localStorageService = new LocalStorageService();
        let shoppingCart = localStorageService.get('shoppingCart');
        shoppingCart = !shoppingCart ? [] : JSON.parse(shoppingCart);
        shoppingCart.push(this.productSKU);
        localStorageService.set('shoppingCart', JSON.stringify(shoppingCart));
        console.log('Producto agregado al carrito');
        alert(`Producto agregado al carrito: ${this.productSKU}`);
    }
}

customElements.define('add-to-cart-button', AddToCartButton);
