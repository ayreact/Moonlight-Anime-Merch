from django.shortcuts import render, redirect, get_object_or_404
from member.models import CustomUser
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

#personal details
@login_required
def account_details(request):
    return render(request, 'account/account.html')

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.phone_number = request.POST['phone_number']
        user.username = request.POST['username']
        #to check if new profile image is provided
        new_profile_img = request.FILES.get('profile_img')
        if new_profile_img:
            user.profile_img = new_profile_img
            
        user.save()
        messages.success(request, 'Personal details have been updated successfully')
        return redirect('account_details')
    return render(request, 'account/account.html')

#account settings
@login_required
def edit_email(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.email = request.POST['email']    
        user.save()
        return redirect('account_details')
    return render(request, 'account/account_settings.html')

@login_required
def edit_user_psw(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        current_password = request.POST['password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        # Check if the current password matches the hashed password in the database
        if not check_password(current_password, user.password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('account_settings')

        # Check if new password and confirm password match
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('account_settings')

        # Set the new password
        user.set_password(new_password)
        user.save()

        # Update session auth hash to prevent the user from being logged out
        update_session_auth_hash(request, user)

        messages.success(request, 'Password updated successfully.')
        return redirect('account_settings')

    return render(request, 'account/account_settings.html')

@login_required
def account_settings(request):
    return render(request, 'account/account_settings.html')

#delete account system
@login_required
def delete_account(request):
    return render(request, 'account/delete_account.html')

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('home')

#log out system
@login_required
def logout_user(request):
    logout(request)
    return redirect('log')