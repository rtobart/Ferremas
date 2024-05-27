from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Categoria, CustomUser, CarritoItem
from .models import CustomUser, CarritoItem
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from django.db.models import Q
from .forms import ProductoForm
import locale
from datetime import datetime
import requests
from django.http import Http404, JsonResponse


def actualizar_moneda(request):
    valor_dolar = moneda()
    return JsonResponse({'valor_dolar': valor_dolar})

def obtener_fecha_actual():
    return datetime.now().strftime('%d-%m-%Y')

fecha_hoy = obtener_fecha_actual()
urlapiusd = f'https://mindicador.cl/api/dolar/{fecha_hoy}'

def moneda():
    global fecha_hoy
    global urlapiusd
    hoy = obtener_fecha_actual()
    
    if hoy != fecha_hoy:
        print(f"Fecha actual diferente a la fecha almacenada se acutaliza la fecha a {hoy}")
        fecha_hoy = hoy
        urlapiusd = f'https://mindicador.cl/api/dolar/{fecha_hoy}'

    response = requests.get(urlapiusd)
    data = response.json()
    valorusd = None

    if response.status_code == 200:
        valorusd = data["serie"][0]["valor"]
        print("Valor del dólar:", valorusd)
    else:
        print("No se pudo obtener el valor del dólar")
    return (valorusd)

def ingreso(request):
    if request.method == 'GET':
        return render(request, 'ingreso.html',{
            'form': AuthenticationForm
         })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'ingreso.html',{
                'form': AuthenticationForm,
                'error': 'Usuario o Contraseña incorrecta'
            })
        else:
            login(request, user)
            CarritoItem.objects.all().delete()
            return redirect('home')  
   
   
def cerrar(request):
    logout(request)
    CarritoItem.objects.all().delete()
    return redirect('home')  
   
#@login_required 
def crear(request):
    if request.method == 'POST':
        try:
            form = ProductoForm(request.POST, request.FILES)
            rol = request.user.rol
            if form.is_valid():
                if user_passes_test(rol == 'admin' or rol == 'bodeguero' or rol == 'vendedor'): # Revisar condiciones
                    new_product = form.save(commit=False)
                    new_product.user = request.user
                    new_product.save()
                    print(request.POST, request.FILES)
                    return redirect('home')
        except ValueError:
            print(request.POST)
            return render(request, 'crear.html', {
                'form': ProductoForm(),
                'error': 'Por favor, valide los datos'
            })
    else:
        return render(request, 'crear.html', {
            'form': ProductoForm(),
        })
        
def actualizar(request, product_id):
    if request.method == 'GET':
        product = get_object_or_404(Producto, pk=product_id)
        form = ProductoForm(instance=product)
        return render(request, 'detalle_producto.html',{
            'product':product,
            'form': form
            })
    else:
        try:
            product = get_object_or_404(Producto, pk=product_id)
            form = ProductoForm(request.POST, instance=product)
            form.save()
            return redirect('products')
        except ValueError:
                return render(request, 'detalle_producto.html',{
                'product':product,
                'form': form,
                'error': 'Error al Actualizar'
                }) 
   
def contacto(request):
    return render(request, 'contacto.html', { 
    })
    # if request.method == 'POST':

    #     return render(request, 'contacto.html', {
            
    #         'mensaje': 'Enviado Correctamente',
    #         'script' : 'window.onload = function() {formu()};'      
    #     }, print(request.POST))
    # else:
    #     return render(request, 'contacto.html', { 
    #     })  
    
def buscar(request):
    if request.method == 'GET':
        query = request.GET.get("q")
        if not query:
            context = {'query': query}
            return render(request, 'resultado_busqueda.html', context)

        resultados = Producto.objects.filter(
            Q(user__username__icontains=query) |  # Buscar por nombre de usuario del artista
            Q(titulo__icontains=query) |  # Buscar por título
            Q(id_categoria__categoria__icontains=query)  # Buscar por categoría
        )

        context = {'resultados': resultados, 'query': query}
        return render(request, 'resultado_busqueda.html', context)