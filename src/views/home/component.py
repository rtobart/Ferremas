from django.shortcuts import render
from src.views.category.controller import CategoryController
from src.views.product.controller import ProductController
from src.views.product.component import productos

product_controller = ProductController()
category_controller = CategoryController()

def home(request):
    products = product_controller.get_all()
    categories = category_controller.get_all()
    
    if request.user.is_authenticated:
        user = request.user
        productos_by_user = productos.filter(user=user)
        num_productos = productos_by_user.count()
        
        context = {
            'productos': products,
            'num_productos': num_productos,
            'categorias': categories,
            #'usuarios': usuarios
        }
        return render(request, 'home.html', context)
    else:
        context = {
            'productos': products,
            'categorias': categories,
        }
        return render(request, 'home.html', context)