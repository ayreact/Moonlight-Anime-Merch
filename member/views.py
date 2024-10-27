from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .models import CustomUser
from django.contrib.auth import login, get_backends
import re

def sign(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone_number = request.POST['phone_number']
        profile_img = request.FILES.get('profile_img')

        # Password validation
        if (
            len(password) >= 8 and
            re.search(r"[A-Z]", password) and
            re.search(r"[a-z]", password) and
            re.search(r"\d", password) and
            re.search(r"[@$!%*_?&#]", password)
        ):
            if password == confirm_password:
                # Check if email or username already exists
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, f'"{email}" email already exists')
                elif CustomUser.objects.filter(username=username).exists():
                    messages.error(request, f'"{username}" username already exists')
                else:
                    # Create the user
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

                    # Automatically log in the user
                    for backend in get_backends():
                        if hasattr(backend, 'get_user') and user == backend.get_user(user.pk):
                            login(request, user, backend='{}.{}'.format(backend.__module__, backend.__class__.__name__))
                            return redirect('home')
                    
                    # Raise an error if no backend is found
                    messages.error(request, 'An error occurred while logging in. Please try again.')
                    return redirect('log')
            else:
                messages.error(request, 'Both passwords do not match')
        else:
            messages.error(request, 'Password must match required format')

    return render(request, 'member/sign.html')

def log(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            # Loop through available backends to find the correct one
            for backend in get_backends():
                if hasattr(backend, 'get_user') and user == backend.get_user(user.pk):
                    # Log in the user with the identified backend
                    login(request, user, backend='{}.{}'.format(backend.__module__, backend.__class__.__name__))
                    return redirect('home')
            # Raise an error if no backend is found
            messages.error(request, 'Could not log in with the provided credentials.')
            return redirect('log')
        else:
            # Authentication failed
            messages.error(request, 'Invalid Username or Password')
            return redirect('log')
    else:
        # Render the login form if the request is GET
        return render(request, 'member/log.html')