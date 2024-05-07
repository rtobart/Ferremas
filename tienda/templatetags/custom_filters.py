from django import template
from tienda.models import Producto

register = template.Library()

@register.filter
def get_item_from_cart(cart, product_id):
    product = Producto.objects.get(pk=product_id)
    return {'producto': product, 'precio_unitario': product.precio, 'subtotal': product.precio * cart[product_id]}
