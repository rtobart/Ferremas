from django.contrib import admin
from django.urls import path

from tienda import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('productos/', views.home, name='productos'),
    path('contacto/', views.home, name='contacto'),
    path('registrar/', views.registrar, name='registrar'),
    path('ingreso/', views.ingreso, name='ingreso'),
    path('cerrar/', views.cerrar, name='cerrar'),
    path('buscar/', views.buscar, name='buscar'),
    path('crear/', views.crear, name='crear'),
    path('borrar/', views.home, name='borrar'),
    path('producto/<int:product_id>/', views.actualizar, name='actualizar'),
    path('detalle/<int:product_id>/', views.detalle, name='detalle'),
    path('categoria/<int:id_categoria>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('carrito/', views.carrito, name='carrito'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

