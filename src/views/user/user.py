class User:
    def __init__(self, mail, password, shopping_cart=None):
        self.mail = mail
        self.password = password
        self.shopping_cart = shopping_cart
