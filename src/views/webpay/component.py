from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from src.services.apiFerramas import ApiFerramasService
from src.views.user.controller import UserController
from src.views.webpay.controller import TransactionController

user_controller = UserController()
transaction_controller = TransactionController()

def webpay(request, totalCLP, cartId):
    cartId = cartId.replace('"', '')
    url = f'https://web-ferremas.onrender.com/order/{cartId}'
    # url = f'http://127.0.0.1:8000/order/{cartId}'
    body = {
            "uyOrder": '00001', 
            "sessionId":  '00001', 
            "amount": totalCLP, 
            "returnUrl": url,
            "cartId": cartId,
    }
    res = transaction_controller.create(body)
    print('res', res)
    context = {
        "totalCLP": totalCLP,
        "token": res['token'],
        "url": res['url']
    }
    return render(request, 'webpay.html', context)