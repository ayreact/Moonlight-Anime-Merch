from django.shortcuts import render, redirect, get_object_or_404
from .models import new_product, team, New_task, blog
from member.models import CustomUser
from products.models import Order, OrderProduct
from nobodyknows.models import user_contact_review
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
import re
from django.db.models import Q

def superuser_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_superuser,
        login_url='/log/'
    )(view_func)
    return decorated_view_func

#Dashboard
@superuser_required
@login_required
def dashboard(request):
    num_product = new_product.objects.all()
    num_user = CustomUser.objects.all()
    num_message = user_contact_review.objects.all()
    num_order = Order.objects.all()
    
    product_num = len(num_product)
    user_num = len(num_user)
    message_num = len(num_message)
    order_num = len(num_order)
    
    context = {
        'product_num': product_num,
        'user_num': user_num,
        'order_num': order_num,
        'message_num': message_num
    }
    return render(request, 'admins/dashboard.html', context)

#Users
@superuser_required
@login_required
def add_member(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone_number = request.POST['phone_number']
        profile_img = request.FILES.get('profile_img')
        
        if (
            len(password) >= 8 and
            re.search(r"[A-Z]", password) and
            re.search(r"[a-z]", password) and
            re.search(r"\d", password) and
            re.search(r"[@$!%*_?&#]", password)
        ):
            if password == confirm_password:
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, f'"{email}" email already exists')
                elif CustomUser.objects.filter(username=username).exists():
                    messages.error(request, f'"{username}" username already exists')
                else:
                    user = CustomUser.objects.create_user(
                        email=email, 
                        password=password, 
                        username=username, 
                        first_name=first_name, 
                        last_name=last_name, 
                        phone_number=phone_number, 
                        profile_img=profile_img
                    )
                    user.save()
                    messages.success(request, f'{username} - Account Created Successfully')
                    return redirect('add_member')
            else:
                messages.error(request, 'Both passwords do not match')
        else:
            messages.error(request, 'Password must match required format')
    return render(request, 'admins/add_member.html')

@superuser_required
@login_required
def manage_member(request):
    member_list = CustomUser.objects.all()
    query = request.GET.get('query', '')
    results = []
    if (query != ''):
        results = CustomUser.objects.filter(
            Q(id__icontains = query)
        )
        context = {
            'member_list': results,
            'query': query
        }
    else:
        context = {
            'member_list': member_list
        }
    return render(request, 'admins/manage_members.html', context)

@superuser_required
@login_required
def view_member(request, member_id):
    member = get_object_or_404(CustomUser, id=member_id)
    return render(request, 'admins/member_detail.html', {'member':member})

@superuser_required
@login_required
def delete_member_alt(request, member_id):
    member = get_object_or_404(CustomUser, id=member_id)
    return render(request, 'admins/delete_member.html', {'member':member})

@superuser_required
@login_required
def delete_member(request, member_id):
    member = get_object_or_404(CustomUser, id=member_id)
    member.delete()
    messages.success(request, f"User {member.username}'s account has been deleted successfully.")
    return redirect('manage_member')

#Team
@superuser_required
@login_required
def add_team(request):
    if request.method == "POST":
        name = request.POST['name']
        position = request.POST['position']
        email = request.POST['email']
        whatsapp = request.POST['whatsapp']
        instagram = request.POST['instagram']
        twitter = request.POST['twitter']
        phone_number = request.POST['phone_number']
        user_img = request.FILES.get('user_img')
        user_cover = request.FILES.get('user_cover')
        
        TeamMember = team(
            name=name,
            position=position,
            email=email,
            whatsapp=whatsapp,
            instagram=instagram,
            twitter=twitter,
            phone_number=phone_number,
            user_img=user_img,
            user_cover=user_cover
        )
        TeamMember.save()
        messages.success(request, f'"{name}" has been added as team member')
        return redirect('add_team')
    return render(request, 'admins/add_team.html')

@superuser_required
@login_required
def manage_team(request):
    team_members = team.objects.all()
    query = request.GET.get('query', '')
    results = []
    if (query != ''):
        results = team.objects.filter(
            Q(name__icontains = query) |
            Q(position__icontains = query)
        )
        context = {
            'team_members': results,
            'query': query
        }
    else:
        context = {
            'team_members': team_members
        }
    return render(request, 'admins/manage_team.html', context)

@superuser_required
@login_required
def edit_team(request, team_id):
    team_member = get_object_or_404(team, id=team_id)
    if request.method == 'POST':
        team_member.name = request.POST['name']
        team_member.position = request.POST['position']
        team_member.email = request.POST['email']
        team_member.whatsapp = request.POST['whatsapp']
        team_member.instagram = request.POST['instagram']
        team_member.twitter = request.POST['twitter']
        team_member.phone_number = request.POST['phone_number']
        
        new_user_img = request.FILES.get('user_img')
        if new_user_img:
            team_member.user_img = new_user_img
        team_member.save()
        messages.success(request, f'Product "{team_member.name}" has been updated successfully')
        return redirect('edit_team', team_member.id)
    return render(request, 'admins/edit_team.html', {'team_member':team_member})

@superuser_required
@login_required
def delete_team_member(request, team_id):
    team_member = get_object_or_404(team, id=team_id)
    team_member.delete()
    messages.success(request, f'"{team_member.name}" has been deleted successfully')
    return redirect('manage_team')

@superuser_required
@login_required
def delete_team(request):
    team_members = team.objects.all()
    team_members.delete()
    messages.success(request, 'All team members have been deleted successfully')
    return redirect('manage_team')

#Products
@superuser_required
@login_required
def add_product(request):
    if request.method == "POST":
        product_name = request.POST['product_name']
        product_price = request.POST['product_price']
        product_desc = request.POST['product_desc']
        product_rating = request.POST['product_rating']
        product_quantity = request.POST['product_quantity']
        product_img = request.FILES.get('product_img')
        product_category = request.POST['product_category']
        discount_value = 0
        
        NewProduct = new_product(
            product_name=product_name, 
            product_price=product_price,
            discount_value=discount_value,
            actual_prod_price=product_price,
            product_desc=product_desc, 
            product_quantity=product_quantity,
            product_rating=product_rating,
            product_img=product_img,
            product_category=product_category
            )
        NewProduct.save()
        messages.success(request, f'"{product_name}" has been added successfully')
        return redirect('add_product')
    return render(request, 'admins/add_products.html')

@superuser_required
@login_required
def manage_product(request):
    product_list = new_product.objects.all()
    query = request.GET.get('query', '')
    results = []
    if (query != ''):
        results = new_product.objects.filter(
            Q(id__icontains = query) | 
            Q(product_name__icontains = query) | 
            Q(product_category__icontains = query)
        )
        context = {
            'product_list': results,
            'query': query
        }
    else:
        context = {
            'product_list': product_list
        }
    return render(request, 'admins/manage_products.html', context)

@superuser_required
@login_required
def edit_product(request, product_id):
    product = get_object_or_404(new_product, id=product_id)
    
    if request.method == 'POST':
        product.product_name = request.POST['product_name']
        product.product_desc = request.POST['product_desc']
        product.product_rating = request.POST['product_rating']
        product.product_category = request.POST['product_category']
        
        discount_value = request.POST['discount_value']
        
        try:
            discount_value_int = int(discount_value)
        except ValueError:
            discount_value_int = 0  # Default to 0 if the conversion fails
            
        product.discount_value = discount_value
            
        actual_prod_price = product.actual_prod_price
        
        actual_prod_price_float = float(actual_prod_price)
        
        # Calculate the discounted price if a discount is applied
        if discount_value_int > 0:
            product.actual_prod_price = actual_prod_price_float
            product.product_price = actual_prod_price_float - ((discount_value_int / 100) * actual_prod_price_float)
        elif discount_value_int == 0:
            product.product_price = product.actual_prod_price
        else:
            product.product_price = actual_prod_price
        
        new_quantity = request.POST['product_quantity']
        add_quantity = request.POST['product_add_quantity']
        new_product_img = request.FILES.get('product_img')
        
        if new_quantity:
            try:
                new_quantity_int = int(new_quantity)
                if new_quantity_int > product.product_quantity:
                    product.product_quantity = 0
                else:
                    product.product_quantity -= new_quantity_int
            except ValueError:
                messages.error(request, 'Invalid product quantity. Please enter a valid integer.')
                return render(request, 'admins/edit_product.html', {'product': product})
            
        if add_quantity:
            try:
                add_quantity_int = int(add_quantity)
                product.product_quantity += add_quantity_int
            except ValueError:
                messages.error(request, 'Invalid product quantity. Please enter a valid integer.')
                return render(request, 'admins/edit_product.html', {'product': product})
        
        if new_product_img:
            product.product_img = new_product_img
        
        product.save()
        messages.success(request, f'Product "{product.product_name}" has been updated successfully')
        return redirect('edit_product', product.id)
    
    return render(request, 'admins/edit_product.html', {'product': product})

@superuser_required
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(new_product, id=product_id)
    product.delete()
    messages.success(request, f'"{product.product_name}" has been deleted successfully')
    return redirect('manage_product')

@superuser_required
@login_required
def delete_all_products(request):
    all_products = new_product.objects.all()
    all_products.delete()
    messages.success(request, 'All products have been deleted successfully')
    return redirect('manage_product')

#User messages
@superuser_required
@login_required
def user_message(request):
    user_messages = user_contact_review.objects.all()
    query = request.GET.get('query', '')
    results = []
    if (query != ''):
        results = user_contact_review.objects.filter(
            Q(name__icontains = query) | 
            Q(subject__icontains = query) | 
            Q(message__icontains = query)
        )
        context = {
            'user_messages': results,
            'query': query
        }
    else:
        context = {
            'user_messages': user_messages
        }
    return render(request, 'admins/contact_messages.html', context)

@superuser_required
@login_required
def message_detail(request, message_id):
    message_detail = get_object_or_404(user_contact_review, id=message_id)
    return render(request, 'admins/message_detail.html', {'message_detail': message_detail})

@superuser_required
@login_required
def delete_message(request, message_id):
    users_message = get_object_or_404(user_contact_review, id=message_id)
    users_message.delete()
    messages.success(request, f"{users_message.name}'s message has been deleted successfully")
    return redirect('user_messages')

@superuser_required
@login_required
def delete_all_messages(request):
    all_messages = user_contact_review.objects.all()
    all_messages.delete()
    messages.success(request, 'All messages have been deleted successfully')
    return redirect('user_messages')

#Orders
@superuser_required
@login_required
def all_orders(request):
    orders = Order.objects.all()
    query = request.GET.get('query', '')
    results = []
    if (query != ''):
        results = Order.objects.filter(
            Q(id__icontains = query)
        )
        context = {
            'orders': results,
            'query': query
        }
    else:
        context = {
            'orders': orders
        }
    return render(request, 'admins/all_orders.html', context)

@superuser_required
@login_required
def new_orders(request):
    orders = Order.objects.all()
    query = request.GET.get('query', '')
    results = []
    if (query != ''):
        results = Order.objects.filter(
            Q(id__icontains = query) |
            Q(delivery__icontains = query)
        )
        context = {
            'orders': results,
            'query': query
        }
    else:
        context = {
            'orders': orders
        }
    return render(request, 'admins/new_orders.html', context)

@superuser_required
@login_required
def complete_orders(request):
    orders = Order.objects.all()
    query = request.GET.get('query', '')
    results = []
    if (query != ''):
        results = Order.objects.filter(
            Q(id__icontains = query)
        )
        context = {
            'orders': results,
            'query': query
        }
    else:
        context = {
            'orders': orders
        }
    return render(request, 'admins/complete_orders.html', context)

@superuser_required
@login_required
def order_ref(request):
    orders = OrderProduct.objects.all()
    query = request.GET.get('query', '')
    results = []

    if query:
        results = OrderProduct.objects.filter(
            Q(order__id__icontains=query)
        )
        context = {
            'orders': results,
            'query': query
        }
    else:
        context = {
            'orders': orders
        }
    return render(request, 'admins/order_ref.html', context)

@superuser_required
@login_required
def order_product(request, product_id):
    product_detail = get_object_or_404(new_product, id=product_id)
    return render(request, 'admins/order_product.html', {'product_detail':product_detail})

@superuser_required
@login_required
def order_detail(request, order_id, user_id):
    order_details = get_object_or_404(Order, id=order_id)
    user_details = get_object_or_404(CustomUser, id=user_id)
    
    context = {
        'order_details':order_details,
        'user_details':user_details
    }
    return render(request, 'admins/order_detail.html', context)

@superuser_required
@login_required
def order_complete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.completed += 1
    
    order.save()
    messages.success(request, f'Order {order.id} completed successfully.')
    return redirect('new_orders')

#Blog
def new_blog(request):
    #add blog
    if request.method == 'POST':
        main_topic = request.POST['main_topic']
        main_body_first = request.POST['main_body_first']
        main_body_sec = request.POST['main_body_sec']
        main_body_third = request.POST['main_body_third']
        main_blockquote = request.POST['main_blockquote']
        sub_topic_first = request.POST['sub_topic_first']
        sub_content_first = request.POST['sub_content_first']
        sub_topic_sec = request.POST['sub_topic_sec']
        sub_content_sec = request.POST['sub_content_sec']
        article_tags = request.POST['article_tags']
        article_category = request.POST['article_category']
        author = request.POST['author']
        main_img = request.FILES.get('main_img')
        sub_img = request.FILES.get('sub_img')
        
        NewBlog = blog(
            main_topic = main_topic,
            main_body_first = main_body_first,
            main_body_sec = main_body_sec,
            main_body_third = main_body_third,
            main_blockquote = main_blockquote,
            sub_topic_first = sub_topic_first,
            sub_content_first = sub_content_first,
            sub_topic_sec = sub_topic_sec,
            sub_content_sec = sub_content_sec,
            article_tags = article_tags,
            article_category = article_category,
            author = author,
            main_img = main_img,
            sub_img = sub_img
        )
        NewBlog.save()
        messages.success(request, f'Article {NewBlog.id} has been added to the blog.')
        return redirect('new_blog')
    
    #system to get all authors(team members)
    team_members = team.objects.all()
    
    context = {
        'team_members':team_members,
    }
    return render(request, 'admins/new_blog.html', context)

def manage_blog(request):
    blog_list = blog.objects.all()
    
    query = request.GET.get('query', '')
    results = []

    if query:
        results = blog.objects.filter(
            Q(order__id__icontains=query)
        )
        context = {
            'blog_list': results,
            'query': query
        }
    else:
        context = {
            'blog_list': blog_list
        }
    return render(request, 'admins/manage_blog.html', context)

def edit_blog(request, blog_id):
    return render(request, 'admins/edit_blog.html')

def delete_blog(request, blog_id):
    main_blog = get_object_or_404(blog, id=blog_id)
    main_blog.delete()
    
    return redirect('manage_blog')

def delete_all_blog(request):
    blog_list = blog.objects.all()
    blog_list.delete()
    
    return redirect('manage_blog')

#Tasks
@superuser_required
@login_required
def tasks(request):
    if request.method == "POST":
        new_task = request.POST['new_task']
        
        NewTask = New_task(
            new_task=new_task
        )
        
        NewTask.save()
        return redirect('dashboard')
    
    all_tasks = New_task.objects.all()
    print(all_tasks)
    return render(request, 'admins/includes/tasks.html', {'all_tasks':all_tasks})