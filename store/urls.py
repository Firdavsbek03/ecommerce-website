from django.urls import path
from .views import store,cart,checkout,update_item,process_order

urlpatterns=[
    path("",store,name="store"),
    path("cart/",cart,name="cart"),
    path("checkout/",checkout,name="checkout"),
    path("update_item/",update_item,name='update-item'),
    path("process_order/",process_order,name="process-order"),
]