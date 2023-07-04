from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True)
    name=models.CharField(max_length=250)
    email=models.EmailField(max_length=250)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    complete=models.BooleanField(default=False)
    transaction_id=models.CharField(max_length=150)
    date_ordered=models.DateTimeField(auto_now_add=True)

    @property
    def cart_total_price(self):
        total=sum([item.total_price for item in self.orderitem_set.all()])
        return total

    @property
    def cart_total_items(self):
        total = sum([item.quantity for item in self.orderitem_set.all()])
        return total

    @property
    def shipping(self):
        shipping=False
        for item in self.orderitem_set.all():
            if not item.product.digital:
                shipping=True
        return shipping

    def __str__(self):
        return str(self.id)


class Product(models.Model):
    name=models.CharField(max_length=250)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to="product",blank=True,null=True)
    digital=models.BooleanField(default=False)

    @property
    def get_image_url(self):
        try:
            url=self.image.url
        except:
            url="../static/images/default.jpg"
        return url

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField(default=0)
    date_ordered=models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.quantity*self.product.price


class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    address=models.CharField(max_length=250)
    city=models.CharField(max_length=250)
    state=models.CharField(max_length=250)
    zipcode=models.CharField(max_length=250)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
