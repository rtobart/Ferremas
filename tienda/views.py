from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Categoria, CustomUser, CarritoItem
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from django.db.models import Q
from .forms import ProductoForm
import locale
from datetime import datetime
import requests
from django.http import JsonResponse

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


def home(request): #Solo inicio de la página
    productos = Producto.objects.filter(aprobado=True, relevante=True).order_by('-aprobado')
    categorias = Categoria.objects.all()
    
    if request.user.is_authenticated:
        user = request.user
        productos_by_user = productos.filter(user=user)
        num_productos = productos_by_user.count()
        
        context = {
            'productos': productos,
            'num_productos': num_productos,
            'categorias': categorias,
            #'usuarios': usuarios
        }
        return render(request, 'home.html', context)
    else:
        context = {
            'productos': productos,
            'categorias': categorias,
            #'usuarios': usuarios
        }
        return render(request, 'home.html', context)
    
def productos(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    context = {
        'productos': productos,
        'categorias': categorias
    }
    return render(request, 'productos.html', context)
    
    
    
    
#@login_required   #Desactivado para pruebas    
def registrar(request):
    if request.method == 'GET':
        return render(request, 'registrar.html',{
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = CustomUser.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'registrar.html',{
                    'form': UserCreationForm,
                    "error": 'Usuario ya existe'
                })
        return render(request, 'registrar.html',{
                    'form': UserCreationForm,
                    "error": 'Contraseñas no coinciden.'
                })  
   
def carrito(request):
    # Obtener el carrito del request
    cart = request.session.get('cart', {})
    items = []
    total_carrito = 0
    
    # Recorrer los elementos del carrito y calcular el total
    for item_id, quantity in cart.items():
        product = get_object_or_404(Producto, pk=item_id)
        subtotal = product.precio * quantity
        items.append({'id':item_id,'product': product, 'quantity': quantity,
                      'precio': product.precio,'imagen':product.imagen, 'subtotal': subtotal})
        total_carrito += subtotal
    return render(request, 'carrito.html', {'items': items, 'total_carrito': total_carrito})

def agregar_al_carrito(request, id):
    # Obtener el ID del producto y la cantidad del POST request
    product_id = id
    quantity = int(request.POST.get('quantity', 1))

    # Obtener el carrito del request
    cart = request.session.get('cart', {})

    # Actualizar el carrito con el nuevo artículo
    cart[product_id] = cart.get(product_id, 0) + quantity

    # Guardar el carrito en la sesión del usuario
    request.session['cart'] = cart
    print(cart)
    return redirect('carrito')

def eliminar_del_carrito(request, product_id):
    # Obtener el carrito del request
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    # Eliminar el producto del carrito
    if product_id_str in cart:
        print("Eliminando producto", product_id_str)
        del cart[product_id_str]

    # Guardar el carrito actualizado en la sesión del usuario
    request.session['cart'] = cart

    return redirect('carrito')

def vaciar_carrito(request):
    # Vaciar el carrito eliminando todos los elementos
    request.session['cart'] = {}

    return redirect('carrito')


def aumentar_cantidad(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        cart[product_id_str] += 1
    request.session['cart'] = cart
    return redirect('carrito')

def disminuir_cantidad(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart and cart[product_id_str] > 1:
        cart[product_id_str] -= 1
    request.session['cart'] = cart
    return redirect('carrito')

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
        
def detalle(request, product_id):
        product = get_object_or_404(Producto, pk=product_id)
        form = ProductoForm(instance=product)
        return render(request, 'detalle.html',{
            'product':product,
            'form': form
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
   
def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id_categoria=categoria_id)
    productos_categoria = Producto.objects.filter(id_categoria=categoria)
    for producto in productos_categoria:
        producto.precio_formateado = locale.format_string("%d", producto.precio, grouping=True)

    context = {
        'categorias': categoria,
        'productos': productos_categoria
    }
    return render(request, 'productos_por.html', context)   
   
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