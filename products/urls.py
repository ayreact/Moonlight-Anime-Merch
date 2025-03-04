from django.urls import path
from .views import (
    product, product_details, add_to_cart, cart, update_cart_quantity, 
    remove_from_cart, proceed_to_checkout, checkout, order_checkout
)

urlpatterns = [
    # Product details - more specific pattern
    path('product_details/<int:product_id>/', product_details, name='product_details'),
    
    # Cart system - more specific patterns
    path('add-to-cart/<int:product_id>/<str:from_loc>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('update-cart-quantity/<int:cart_product_id>/<int:product_id>/<str:action>/<str:from_loc>/', update_cart_quantity, name='update_cart_quantity'),
    path('remove-from-cart/<int:cart_product_id>/<str:from_loc>/', remove_from_cart, name='remove_from_cart'),
    
    # Checkout order system - more specific patterns
    path('proceed_to_checkout/', proceed_to_checkout, name='proceed_to_checkout'),
    path('checkout/', checkout, name='checkout'),
    path('order_checkout/<int:order_id>/<int:payment_id>/', order_checkout, name='order_checkout'),
    
    # Shop - more general pattern, placed last
    path('<str:categ>', product, name='product'),
]