from django.shortcuts import get_object_or_404, redirect, render
import json
from src.views.product.controller import ProductController
from src.views.category.controller import CategoryController
from src.views.shoppingCart.controller import ShopingCartController
import jwt

product_controller = ProductController()
category_controller = CategoryController()
shopping_cart_controller = ShopingCartController()

def carrito(request):
    items = request.session.get('items', '[]')
    products = []
    for item in items:
        product = product_controller.get_by_sku(item)
        products.append(product)
    categories = category_controller.get_all()
    context = {
        'productos': products,
        'categorias': categories
    }
    return render(request, 'carrito.html', context)

def loadcart(request, items, mail):
    request.session['items'] = items
    shopping_cart_controller.add_product_to_shopping_cart(mail, items)
    return redirect('carrito')

def precart(request):
    return render(request, 'precart.html')
