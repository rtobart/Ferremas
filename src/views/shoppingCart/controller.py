from typing import List
from src.services.httpService import HttpService
from src.services.apiFerramas import ApiFerramasService
from src.interfaces.get import GetInterface
from src.interfaces.post import PostInterface
from src.interfaces.response import Response

http_service = HttpService()
api_ferramas_service = ApiFerramasService(http_service)

class ShopingCartController:
    def __init__(self):
        self.api_service = api_ferramas_service

    def create_shopping_cart(self, products: List[str], user: str):
        body = {
            "products": products,
            "user": user
        }
        request = PostInterface("shoping-cart", body)
        _response = self.api_service.post(request)
        response = Response(_response['result'], _response['data'])
        shopping_cart_id = response.data['shoppingCartId']
        return shopping_cart_id
    
    def get_shopping_cart(self, mail: str):
        request = GetInterface(f"shoping-cart/mail/{mail}")
        _response = self.api_service.get(request)
        response = Response(_response['result'], _response['data'])
        return response.data
    
    def add_product_to_shopping_cart(self, mail: str, products: str):
        body = {
            'mail': mail,
            'tools': products
        }
        request = PostInterface("shoping-cart/add", body)
        _response = self.api_service.post(request)
        response = Response(_response['result'], _response['data'])
        return response.data
