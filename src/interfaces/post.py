class PostInterface:
    def __init__(self, path: str, auth_token=None, body=None):
        self.path = path
        self.auth_token = auth_token
        self.body = body