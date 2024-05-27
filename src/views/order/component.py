from django.shortcuts import render
from src.views.category.controller import CategoryController
from src.views.product.controller import ProductController

product_controller = ProductController()
category_controller = CategoryController()

def order(request, order_id):
    context = {
        'order_id': order_id,
    }
    return render(request, 'order.html', context)
