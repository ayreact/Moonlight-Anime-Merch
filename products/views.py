from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import new_product, Cart, CartProduct, Order, OrderProduct
from django.db.models import Q
from urllib.parse import urlencode

#products system
def product(request, categ):
    product_list_db = list(new_product.objects.all())
    
    product_list = []
    if categ == 'all':
        product_list = product_list_db
    else:
        for a_product in product_list_db:
            if a_product.product_category.lower() == categ:
                product_list.append(a_product)
    
    cart = Cart.objects.filter(user=request.user).first() if request.user.is_authenticated else None
    cart_products = CartProduct.objects.filter(cart=cart) if cart else []
    
    # Dictionary to map product IDs to their CartProduct objects
    cart_product_map = {cp.product_id: cp for cp in cart_products}
    cart_products_id = list(cart_product_map.keys())
    
    product_list.reverse()

    # Search feature
    query = request.GET.get('query', '')
    results = []
    if query:
        results = list(new_product.objects.filter(
            Q(product_name__icontains=query) | 
            Q(product_desc__icontains=query) | 
            Q(product_category__icontains=query)
        ))
        results.reverse()
        context = {
            'product_list': results,
            'query': query,
            'cart_products_id': cart_products_id,
            'cart_product_map': cart_product_map,
        }
    else:
        context = {
            'product_list': product_list,
            'cart_products_id': cart_products_id,
            'cart_product_map': cart_product_map,
        }
    return render(request, 'products/products.html', context)


def product_details(request, product_id):
    product_detail = get_object_or_404(new_product, id=product_id)
    
    cart = Cart.objects.filter(user=request.user).first() if request.user.is_authenticated else None
    cart_products = CartProduct.objects.filter(cart=cart) if cart else []
    
    # Dictionary to map product IDs to their CartProduct objects
    cart_product_map = {cp.product_id: cp for cp in cart_products}
    cart_products_id = list(cart_product_map.keys())
    
    context = {
        'product_detail':product_detail,
            'cart_products_id': cart_products_id,
            'cart_product_map': cart_product_map,
    }
    return render(request, 'products/product_detail.html', context)


#cart system
@login_required
def add_to_cart(request, product_id, from_loc):
    product = get_object_or_404(new_product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
    
    cart_product.product_total = (product.product_price * cart_product.quantity)
    if not created:
        cart_product.quantity += 1
    cart_product.save()
    
    #getting the product category in lowercase(used for the redirect url)
    product_category = product.product_category.lower()
    if from_loc == 'from_prod':
        # Redirect to the product view with the category as a query parameter
        base_url = reverse('product', kwargs={'categ': product_category})
        query_params = {'category': product_category}
        redirect_url = f"{base_url}?{urlencode(query_params)}"
        return redirect(redirect_url)
    elif from_loc == 'from_prod_det':
        return redirect(reverse('product_details', args=[product_id]))
    elif from_loc == 'from_index':
        return redirect('home')

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_products = CartProduct.objects.filter(cart=cart)
    for item in cart_products:
        item.total_price = item.product.product_price * item.quantity
        
    # Calculate the overall total price of the cart
    ovr_total_price = sum(item.total_price for item in cart_products)
    context = {
        'cart': cart,
        'total':ovr_total_price
        }
    return render(request, 'products/cart.html', context)

@login_required
def update_cart_quantity(request, cart_product_id, product_id, action, from_loc):
    cart_product = get_object_or_404(CartProduct, id=cart_product_id)
    product = get_object_or_404(new_product, id=product_id)

    # Adjust quantity based on action
    if action == 'increase':
        cart_product.quantity += 1
    elif action == 'decrease' and cart_product.quantity > 1:
        cart_product.quantity -= 1
    
    # Update the total for the cart product
    cart_product.product_total = cart_product.quantity * product.product_price
    cart_product.save()
    
    # Determine the product category (used for the category query parameter)
    product_category = product.product_category.lower()

    # Determine where to redirect
    if from_loc == 'from_cart':
        return redirect('cart')
    elif from_loc == 'from_prod':
        # Redirect to the product view with the category as a query parameter
        base_url = reverse('product', kwargs={'categ': product_category})
        query_params = {'category': product_category}
        redirect_url = f"{base_url}?{urlencode(query_params)}"
        return redirect(redirect_url)
    elif from_loc == 'from_prod_det':
        return redirect(reverse('product_details', kwargs={'product_id': product_id}))
    elif from_loc == 'from_index':
        return redirect('home')

@login_required
def remove_from_cart(request, cart_product_id, from_loc):
    cart_product = get_object_or_404(CartProduct, id=cart_product_id)
    product_category = cart_product.product.product_category.lower()
    
    # Remove the item from the cart
    cart_product.delete()

    # Determine where to redirect
    if from_loc == 'from_cart':
        return redirect('cart')
    elif from_loc == 'from_prod':
        # Redirect to the product view with the category as a query parameter
        base_url = reverse('product', kwargs={'categ': 'all'})
        query_params = {'category': 'shop_all'}
        redirect_url = f"{base_url}?{urlencode(query_params)}"
        return redirect(redirect_url)
    elif from_loc == 'from_prod_det':
        return redirect(reverse('product_details', kwargs={'product_id': cart_product.product.id}))
    elif from_loc == 'from_index':
        return redirect('home')

#checkout system
@login_required
def proceed_to_checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_products = CartProduct.objects.filter(cart=cart)
    
    for item in cart_products:
        item.total_price = item.product.product_price * item.quantity
        
    # Calculate the overall total price of the cart
    sub_total_price = sum(item.total_price for item in cart_products)
    tax = 0.08 * sub_total_price
    total_price = tax + sub_total_price
    
    context = {
        'cart': cart,
        'sub_total': sub_total_price,
        'tax': tax,
        'total': total_price
    }
    return render(request, 'products/checkout.html', context)

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    order = Order.objects.create(user=request.user, sub_total=0)
    
    for cart_product in cart.cartproduct_set.all():
        OrderProduct.objects.create(
            order=order,
            product=cart_product.product,
            quantity=cart_product.quantity,
            product_total=cart_product.product_total
        )
        
        #update product quantity
        per_product = get_object_or_404(new_product, id=cart_product.product.id)
        print(per_product)
        print(type(per_product))
        print(type(cart_product.quantity))
        per_product.save()
    
    if request.method == "POST":
        delivery = request.POST['delivery']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        
        # Update order details
        order.delivery = delivery
        order.email = email
        order.phone_number = phone_number
        order.sub_total = sum(
            cart_product.product.product_price * cart_product.quantity
            for cart_product in cart.cartproduct_set.all()
        )
        order.tax = 0.08 * order.sub_total
        order.total = order.sub_total + order.tax
        
        order.save()
        
        # Clear the cart
        cart.delete()
        
        # Redirect to the payment initiation page
        return redirect('initiate_payment', order_id=order.id)
    
    # If the method is not POST, render the checkout form
    return render(request, 'products/checkout.html', {'order': order})


@login_required
def order_checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order
        }
    return render(request, 'products/order_checkout.html', context)