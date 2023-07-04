import json
from .models import *


def cookie_cart(request):
    try:
        cart_items = json.loads(request.COOKIES['cart'])
    except:
        cart_items = {}
    ordered_items = []
    order = {"cart_total_price": 0, "cart_total_items": 0, 'shipping': False}
    cart_items_count = order["cart_total_items"]
    try:
        for key in cart_items:
            cart_items_count += cart_items[key]['quantity']

            product = Product.objects.get(id=key)
            total = product.price * cart_items[key]['quantity']

            order['cart_total_price'] += total
            order['cart_total_items'] += cart_items[key]["quantity"]

            item = {
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "get_image_url": product.get_image_url,
                    "price": product.price,
                },
                "quantity": cart_items_count,
                "total_price": total,

            }
            ordered_items.append(item)
            if not product.digital:
                order['shipping'] = True
    except:
        pass
    return {
        "cart_items_count":cart_items_count,
        "order":order,
        "ordered_items":ordered_items
    }


def get_cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        ordered_items = order.orderitem_set.all()
        cart_items_count = order.cart_total_items
    else:
        cookie_data = cookie_cart(request)
        order = cookie_data['order']
        ordered_items = cookie_data['ordered_items']
        cart_items_count = cookie_data['cart_items_count']
    return {
        "cart_items_count":cart_items_count,
        "order":order,
        "ordered_items":ordered_items,
    }


def guest_user_data(request,data):
    print("The user is not logged in..")
    print("COOKIES:", request.COOKIES)

    name = data["user_form_data"]['name']
    email = data['user_form_data']['email']
    cookie_data = cookie_cart(request)
    ordered_items = cookie_data['ordered_items']

    customer,created=Customer.objects.get_or_create(email=email)
    customer.name=name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for order_item in ordered_items:
        OrderItem.objects.create(order=order, product=Product.objects.get(id=order_item['product']['id']),
                                 quantity=order_item['quantity'])
    return order,customer
