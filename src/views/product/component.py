from django.shortcuts import render
from src.views.category.controller import CategoryController
from src.views.product.controller import ProductController

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

def productos_por_categoria(request, categoria_id):
    categorias = category_controller.get_all()
    categoria = categorias.get_by_id(categoria_id)
    productos_categoria = product_controller.get_by_category(categoria_id)
    context = {
        'categorias': categoria,
        'productos': productos_categoria
    }
    return render(request, 'productos_por.html', context)