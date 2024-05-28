from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from src.services.apiFerramas import ApiFerramasService
from src.views.user.controller import UserController
from src.views.webpay.controller import TransactionController
import datetime


user_controller = UserController()
transaction_controller = TransactionController()

def webpay(request, totalCLP, cartId, mail):
    cartId = cartId.replace('"', '')
    url = f'https://web-ferramas.onrender.com/order/{cartId}'
    # url = f'http://127.0.0.1:8000/preorder/'
    now = datetime.datetime.now()
    date_time_string = now.strftime("%Y%m%d%H%M%S")
    uyOrder = date_time_string + mail
    body = {
            "uyOrder": uyOrder, 
            "sessionId":  mail, 
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