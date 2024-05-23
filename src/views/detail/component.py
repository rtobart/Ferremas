from django.http import Http404
from django.shortcuts import render
from src.views.category.controller import CategoryController
from src.views.product.controller import ProductController

product_controller = ProductController()
category_controller = CategoryController()

def detalle(request, product_id):
        categories = category_controller.get_all()
        products = product_controller.get_all()
        product = next((product for product in products if product['sku'] == product_id), None)
        if product is None:
            raise Http404("Producto no existe")
        context = {
            'product': product,
            'categories': categories,
        }
        return render(request, 'detalle.html', context)