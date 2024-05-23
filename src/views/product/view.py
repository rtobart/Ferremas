from django.shortcuts import render
from src.modules.category.controller import CategoryController
from src.modules.product.controller import ProductController

product_controller = ProductController()
category_controller = CategoryController()

def productos(request):
    productos = product_controller.get_all()
    categories = category_controller.get_all()
    context = {
        'productos': productos,
        'categorias': categories
    }
    return render(request, 'productos.html', context)