from .httpService import HttpService

class ApiFerramasService:
    def __init__(self, http_service: HttpService):
        self.http_service = http_service
        self.route = "http://localhost:3000/api/"

    def get(self, request):
        return self.http_service.get(self.route, request)

    def post(self, request):
        return self.http_service.post(self.route, request)

    def patch(self, request):
        return self.http_service.patch(self.route, request)

    def delete(self, request):
        return self.http_service.delete(self.route, request)

    def put(self, request):
        return self.http_service.put(self.route, request)
