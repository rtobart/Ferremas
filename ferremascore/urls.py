from django.contrib import admin
from django.urls import path

from tienda import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('productos/', views.productos, name='productos'),
    path('contacto/', views.contacto, name='contacto'),
    path('registrar/', views.registrar, name='registrar'),
    path('ingreso/', views.ingreso, name='ingreso'),
    path('cerrar/', views.cerrar, name='cerrar'),
    path('buscar/', views.buscar, name='buscar'),
    path('crear/', views.crear, name='crear'),
    path('borrar/', views.home, name='borrar'),
    path('producto/<int:product_id>/', views.actualizar, name='actualizar'),
    path('detalle/<int:product_id>/', views.detalle, name='detalle'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('carrito/', views.carrito, name='carrito'),
    path('carrito/agregar/<int:id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:product_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/aumentar/<int:product_id>/', views.aumentar_cantidad, name='aumentar_cantidad'),
    path('carrito/disminuir/<int:product_id>/', views.disminuir_cantidad, name='disminuir_cantidad'),
    path('actualizar_moneda/', views.actualizar_moneda, name='actualizar_moneda')
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

