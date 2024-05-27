from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from src.views.user.controller import UserController

user_controller = UserController()

def ingreso(request):
    if request.method == 'GET':
        return render(request, 'ingreso.html',{
            'form': UserCreationForm
        })
    else:
        try:
            user_data = {
                'mail': request.POST['email'],
                'password': request.POST['password'],
            }
            token: str = user_controller.login(user_data)
            print(token)
            return redirect('load_user', token=token, mail=user_data['mail'])
        except IntegrityError:
            return render(request, 'ingreso.html',{
                'form': UserCreationForm,
                "error": 'Usuario no encontrado'
            })