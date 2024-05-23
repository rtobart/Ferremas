from src.services.httpService import HttpService
from src.services.apiFerramas import ApiFerramasService
from src.interfaces.get import GetInterface
from src.interfaces.response import Response
from .category import Categories

http_service = HttpService()
api_ferramas_service = ApiFerramasService(http_service)

class CategoryController:
    def __init__(self):
        self.api_service = api_ferramas_service

    def get_all(self):
        request = GetInterface("tool/category")
        _response = self.api_service.get(request)
        response = Response(_response['result'], _response['data'])
        categories = Categories(response.data)
        return categories
