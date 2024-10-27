from django.shortcuts import render, redirect
from .models import user_contact_review, mam_wa_group
from admins.models import team, new_product
from products.models import Cart, CartProduct
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random

#Home page system
def home(request):
    home_prod = list(new_product.objects.all())
    home_prod_rev = home_prod.reverse()
    
    product_list = []
    for product in home_prod:
        product_list.append(product)
        if len(product_list) == 8:
            break
        
    cart = Cart.objects.filter(user=request.user).first() if request.user.is_authenticated else None
    cart_products = CartProduct.objects.filter(cart=cart) if cart else []
    
    # Dictionary to map product IDs to their CartProduct objects
    cart_product_map = {cp.product_id: cp for cp in cart_products}
    cart_products_id = list(cart_product_map.keys())
    
    context = {
        'product_list':product_list,
        'cart_products_id':cart_products_id,
        'cart_product_map':cart_product_map
    }
    
    return render(request, 'nobodyknows/index.html', context)

def about(request):
    Team = team.objects.all()
    return render(request, 'nobodyknows/about.html', {'Team':Team})

def blog(request):
    return render(request, 'nobodyknows/blog.html')

def blog_details(request):
    return render(request, 'nobodyknows/blog_post.html')

@csrf_protect
def contact(request):
    if request.method == "POST":
        y_name = request.POST['name']
        y_email = request.POST['email']
        y_subject = request.POST['subject']
        y_message = request.POST['message']
        
        UserConRev = user_contact_review(name=y_name, email=y_email, subject=y_subject, message=y_message)
        UserConRev.save()
        
        messages.success(request, f'{y_name}, your message has been submitted and would be looked through.')
        return redirect('contact')
    return render(request, 'nobodyknows/contact.html')

@csrf_protect
@login_required
def wa_group(request):
    new_wa = mam_wa_group.objects.create(user=request.user)
    if request.method == 'POST':
        new_wa.wa_number = request.POST['wa_number']
        
        new_wa.save()
        return redirect('wa_success')
    return render(request,'nobodyknows/includes/footer.html')


def wa_success(request):
    return render(request, 'nobodyknows/wa_success.html')