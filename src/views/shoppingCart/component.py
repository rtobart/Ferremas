from django.shortcuts import get_object_or_404, redirect, render
import json
from src.views.product.controller import ProductController
from src.views.category.controller import CategoryController

product_controller = ProductController()
category_controller = CategoryController()


def carrito(request):
    products = product_controller.get_all()
    categories = category_controller.get_all()
    items = request.session.get('items', [])
    print('items:', items)
    context = {
        'productos': products,
        'categorias': categories
    }
    return render(request, 'carrito.html', context)

def loadcart(request, items):
    request.session['items'] = items
    return redirect('carrito')

def precart(request):
    return render(request, 'precart.html')
