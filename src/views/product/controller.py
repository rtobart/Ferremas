from src.services.httpService import HttpService
from src.services.apiFerramas import ApiFerramasService
from src.interfaces.get import GetInterface
from src.interfaces.response import Response
from .product import Products

http_service = HttpService()
api_ferramas_service = ApiFerramasService(http_service)

class ProductController:
    def __init__(self):
        self.api_service = api_ferramas_service

    def get_all(self):
        request = GetInterface("tool")
        _response = self.api_service.get(request)
        response = Response(_response['result'], _response['data'])
        products = Products(response.data)
        return products
    
    def get_by_category(self, category):
        request = GetInterface(f'tool/filter/category/{category}')
        _response = self.api_service.get(request)
        response = Response(_response['result'], _response['data'])
        products = Products(response.data)
        return products
