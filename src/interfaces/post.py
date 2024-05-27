class PostInterface:
    def __init__(self, path: str, body=None, auth_token=None):
        self.path = path
        self.body = body
        self.auth_token = auth_token