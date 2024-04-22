from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Categoria, CustomUser, CarritoItem
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from django.db.models import Q
from .forms import ProductoForm
import locale


def home(request): #Solo inicio de la página
    productos = Producto.objects.filter(aprobado=True, relevante=True).order_by('-aprobado')
    categorias = Categoria.objects.all()
    usuarios = CustomUser.objects.all()
    
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
    if request.user.is_superuser or request.user.is_staff:
        return render(request, 'home.html') #Revisar si se puede redirigir a otra página
    else:
        items = CarritoItem.objects.all()
        total_carrito = sum(item.subtotal() for item in items)
        return render(request, 'carrito.html', {'items': items, 'total_carrito': total_carrito})

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
            form = ProductoForm(request.POST, request.FILES)  # Agregar request.FILES al inicializar el formulario
            rol = request.user.rol
            if form.is_valid():
                if user_passes_test(rol == 'admin' or rol == 'bodeguero' or rol == 'vendedor'):
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