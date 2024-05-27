from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from src.views.user.controller import UserController
from src.views.shoppingCart.controller import ShopingCartController
import json

user_controller = UserController()
shopping_cart_controller = ShopingCartController()

def registrar(request):
    if request.method == 'GET':
        return render(request, 'registrar.html',{
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user_data = {
                    'username': request.POST['username'],
                    'mail': request.POST['email'],
                    'password': request.POST['password1'],
                    "shopingCartId": ""
                }
                exist_user: bool = user_controller.exist_user(request.POST['email'])
                if exist_user:
                    return render(request, 'registrar.html',{
                        'form': UserCreationForm,
                        "error": 'Usuario ya existe'
                    })
                shopping_cart_products = request.POST['shoppingCart']
                shopping_cart_products = json.loads(shopping_cart_products)
                shopping_cart_id = shopping_cart_controller.create_shopping_cart(shopping_cart_products, user_data['mail'])
                user_data["shopingCartId"] = shopping_cart_id
                token = user_controller.register(user_data)
                return redirect('save_token', token=token)
            except IntegrityError:
                return render(request, 'registrar.html',{
                    'form': UserCreationForm,
                    "error": 'Usuario ya existe'
                })
        return render(request, 'registrar.html',{
                    'form': UserCreationForm,
                    "error": 'Contraseñas no coinciden.'
                })  