from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Producto, Categoria, CustomUser
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'rol', 'spam']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('rol', 'spam')}),
    )

class ProductoAdmin(admin.ModelAdmin):
    readonly_fields = ('subida',)
    
admin.site.register(Categoria)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(CustomUser, CustomUserAdmin)