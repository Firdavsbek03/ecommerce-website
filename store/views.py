from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .utils import get_cart_data,guest_user_data
import decimal
import json
import datetime


def store(request):
    card_data = get_cart_data(request)
    products = Product.objects.all()
    return render(request, "store/store.html",
                  context={"products": products, "cart_items_count": card_data["cart_items_count"]})


def cart(request):
    card_data = get_cart_data(request)
    context = {"ordered_items": card_data["ordered_items"], "order": card_data["order"],
               "cart_items_count": card_data["cart_items_count"]}
    return render(request, "store/cart.html", context=context)


def checkout(request):
    card_data=get_cart_data(request)
    context = {"ordered_items": card_data["ordered_items"], "order": card_data["order"],
               "cart_items_count": card_data["cart_items_count"]}
    return render(request, "store/checkout.html", context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    ordered_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        ordered_item.quantity += 1
    elif action == 'remove':
        ordered_item.quantity -= 1
    ordered_item.save()

    if ordered_item.quantity <= 0:
        ordered_item.delete()

    return JsonResponse({"message": "This message is being outputted"})


def process_order(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        order,customer=guest_user_data(request,data)

    order.transaction_id = transaction_id
    total = decimal.Decimal(data["user_form_data"]['total'])
    if total == order.cart_total_price:
        order.complete = True
    order.save()
    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping_form_data']['address'],
            city=data['shipping_form_data']['city'],
            state=data['shipping_form_data']['state'],
            zipcode=data['shipping_form_data']['zipcode']
        )
    return JsonResponse("payment is complete",safe=False)
