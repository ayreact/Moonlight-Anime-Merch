from django.db import models
from django.conf import settings
from admins.models import new_product

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(new_product, through='CartProduct')

    def __str__(self):
        return f"Cart of {self.user.email}"

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(new_product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    product_total = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name} in cart of {self.cart.user.email}"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(new_product, through='OrderProduct')
    sub_total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.IntegerField(default=0)
    delivery = models.TextField(default="")
    email = models.TextField(default="")
    phone_number = models.TextField(default="")

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(new_product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    product_total = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name} in order {self.order.id}"