from typing import List

class Precio:
    def __init__(self, actual: bool, usd: int, fecha_actualizacion_precio: str, clp: int):
        self.actual = actual
        self.USD = usd
        self.fecha_actualizacion_precio = fecha_actualizacion_precio
        self.CLP = clp

class Product:
    def __init__(self, sku: str, activo: bool, precio: List[Precio], categoria: List[str], codigo_producto: str, marca: str, nombre: str, imagen: str, descripcion: str, fecha_creacion: str):
        self.sku = sku
        self.activo = activo
        self.precio = precio
        self.categoria = categoria
        self.codigo_producto = codigo_producto
        self.marca = marca
        self.nombre = nombre
        self.imagen = imagen
        self.descripcion = descripcion
        self.fecha_creacion = fecha_creacion
    def __str__(self):
        return self.nombre

class Products:
    def __init__(self, product_list: List[Product]):
        self.product_list = product_list
    def __getitem__(self, index):
        return self.product_list[index]