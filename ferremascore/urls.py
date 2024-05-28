import ast
from django.contrib import admin
from django.urls import path

from tienda import views
from django.conf import settings
from django.conf.urls.static import static

# VIEWS
from src.views.home.component import home
from src.views.product.component import productos, productos_por_categoria
from src.views.detail.component import detalle
from src.views.shoppingCart.component import carrito, precart, loadcart
from src.views.register.component import registrar
from src.views.savetoken.component import load_user, save_token
from src.views.login.component import ingreso
from django.urls import register_converter
from src.views.order.component import order
from src.views.webpay.component import webpay
from src.views.preorder.component import preorder

class ListConverter:
    regex = '[^/]+'
    def to_python(self, value):
        return ast.literal_eval(value)
    def to_url(self, value):
        return str(value)

register_converter(ListConverter, 'list')


urlpatterns = [
    path('', home, name='home'),
    path('productos/', productos, name='productos'),
    path('detalle/<str:product_id>/', detalle, name='detalle'),
    path('categoria/<str:categoria_id>/', productos_por_categoria, name='productos_por_categoria'),
    path('registrar/', registrar, name='registrar'),
    path('save-token/<str:token>/', save_token, name='save_token'),
    path('load-user/<str:token>/<str:mail>', load_user, name='load_user'),
    path('ingreso/', ingreso, name='ingreso'),
    # path('carrito/', carrito, name='carrito'),
    path('precart/', precart, name='precart'),
    path('loadcart/<list:items>/<str:mail>', loadcart, name='loadcart'),
    path('carrito/', carrito, name='carrito'),
    path('order/<str:order_id>', order, name='order'),
    path('preorder/<str:order_id>', preorder, name='preorder'),
    path('webpay/<int:totalCLP>/<str:cartId>', webpay, name='webpay'),
    
    path('admin/', admin.site.urls),
    path('contacto/', views.contacto, name='contacto'),
    path('cerrar/', views.cerrar, name='cerrar'),
    path('buscar/', views.buscar, name='buscar'),
    path('crear/', views.crear, name='crear'),
    # path('borrar/', views.home, name='borrar'),
    # path('producto/<int:product_id>/', views.actualizar, name='actualizar'),
    # path('carrito/agregar/<int:id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    # path('carrito/eliminar/<int:product_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    # path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    # path('carrito/aumentar/<int:product_id>/', views.aumentar_cantidad, name='aumentar_cantidad'),
    # path('carrito/disminuir/<int:product_id>/', views.disminuir_cantidad, name='disminuir_cantidad'),
    path('actualizar_moneda/', views.actualizar_moneda, name='actualizar_moneda')
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

