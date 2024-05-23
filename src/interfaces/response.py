class result:
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message

class Response:
    def __init__(self, result: result, data):
        self.result = result
        self.data = data