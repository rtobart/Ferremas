from src.services.httpService import HttpService
from src.services.apiFerramas import ApiFerramasService
from src.interfaces.post import PostInterface
from src.interfaces.get import GetInterface
from src.interfaces.response import Response
from src.views.user import user

http_service = HttpService()
api_ferramas_service = ApiFerramasService(http_service)

class UserController:
    def __init__(self):
        self.api_service = api_ferramas_service

    def register(self, user: any):
        request = PostInterface("auth/register", user)
        _response = self.api_service.post(request)
        response = Response(_response['result'], _response['data'])
        token = response.data
        return token
    
    def exist_user(self, user: str):
        request = GetInterface(f"auth/exist/{user}")
        _response = self.api_service.get(request)
        response = Response(_response['result'], _response['data'])
        exist = response.data
        return exist
    
    def login(self, user: any):
        request = PostInterface("auth", user)
        _response = self.api_service.post(request)
        response = Response(_response['result'], _response['data'])
        token = response.data
        print(token)
        return token