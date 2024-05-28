from src.interfaces.post import PostInterface
from src.services.httpService import HttpService
from src.services.apiFerramas import ApiFerramasService
from src.interfaces.get import GetInterface
from src.interfaces.response import Response

http_service = HttpService()
api_ferramas_service = ApiFerramasService(http_service)

class TransactionController:
    def __init__(self):
        self.api_service = api_ferramas_service

    def create(self, body):
        request = PostInterface("transaction", body)
        _response = self.api_service.post(request)
        response = Response(_response['result'], _response['data'])
        print('response', response)
        tx = response.data
        return tx
    
    def commit(self, token):
        request = GetInterface(f"transaction/{token}")
        _response = self.api_service.get(request)
        response = Response(_response['result'], _response['data'])
        print('response', response)
        token = response.data
        return token
    
    def validate(self, order, cart):
        request = GetInterface(f"transaction/{order}/{cart}")
        self.api_service.get(request)

