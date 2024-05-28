from django.shortcuts import render

from src.views.shoppingCart.controller import ShopingCartController

shopping_cart_controller = ShopingCartController()

def save_token(request, token):
    return render(request, 'escribir_token.html', {'token': token})

def load_user(request, token, mail):
    shopping_cart = shopping_cart_controller.get_shopping_cart(mail)
    print('shopping_cart ', shopping_cart)
    shopping_cart_products = shopping_cart['l_products']
    context = {
        'token': token, 
        'shopping_cart': shopping_cart_products,
        'shopping_cart_id': shopping_cart['_id'],
        'mail': mail,
        }
    return render(request, 'escribir_token.html', context)