from django.contrib import admin
from .models import new_product, Cart, CartProduct, Order, OrderProduct

admin.site.register(new_product)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)
admin.site.register(OrderProduct)