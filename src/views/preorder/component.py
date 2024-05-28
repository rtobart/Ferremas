from django.shortcuts import get_object_or_404, redirect, render
from src.views.product.controller import ProductController
from src.views.category.controller import CategoryController
from src.views.shoppingCart.controller import ShopingCartController
from src.views.webpay.controller import TransactionController

product_controller = ProductController()
category_controller = CategoryController()
shopping_cart_controller = ShopingCartController()
transaction_controller = TransactionController()

def preorder(request, order_id, cart_id):
    token_ws = request.GET.get('token_ws', '')
    response = transaction_controller.commit(token_ws)
    print('response', response['status'])
    status = response['status']
    context = {
        'status': status,
        'order_id': order_id,
    }
    if status == 'AUTHORIZED':
        transaction_controller.validate(order_id, cart_id)
    return render(request, 'preorder.html', context)

