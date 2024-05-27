import requests
from src.interfaces.get import GetInterface
from src.interfaces.post import PostInterface

def error_format(self, response):
    return {
        'status': response.status_code,
        'error': response.text
    }
class HttpService:
    def __init__(self):
        self.session = requests.Session()

    def get(self, route: str, request: GetInterface, headers=None):
        try:
            response = self.session.get(f"{route}{request.path}", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError:
            return self.error_format(response)

    def post(self, route: str, request: PostInterface, headers=None):
        try:
            response = self.session.post(f"{route}{request.path}", json=request.body, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError:
            return self.error_format(response)

    def patch(self, route: str, request: GetInterface, headers=None):
        try:
            response = self.session.patch(f"{route}{request.path}", json=request['body'], headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError:
            return self.error_format(response)

    def put(self, route: str, request: PostInterface, headers=None):
        try:
            response = self.session.put(f"{route}{request.path}", json=request['body'], headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError:
            return self.error_format(response)

    def delete(self, route: str, request: GetInterface, headers=None):
        try:
            response = self.session.delete(f"{route}{request.path}", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError:
            return self.error_format(response)