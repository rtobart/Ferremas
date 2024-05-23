from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('vendedor', 'Vendedor'),
        ('bodeguero', 'Bodeguero'),
        ('contador', 'Contador'),
        ('default', 'Default'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='default')
    spam = models.BooleanField(default=False)
    
# Create your models here.
class Categoria(models.Model):
    id_categoria  = models.AutoField(db_column='idCategoria', primary_key=True) 
    categoria     = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return str(self.categoria)
    
class Producto(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.PositiveIntegerField(null=True)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
    subida = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)
    relevante = models.BooleanField(default=False)
    comentario = models.TextField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo
    
class CarritoItem(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.PositiveIntegerField(default=0)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.producto.titulo} - {self.usuario.username if self.usuario else 'Usuario Anónimo'}"