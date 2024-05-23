from typing import List
from .producto import Producto

class Carrito:
    def __init__(self, producto: List[Producto]):
        self.producto = producto