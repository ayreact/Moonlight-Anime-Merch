from . import views
from django.urls import path

urlpatterns = [
   #personal details
   path('', views.account_details, name='account_details'),
   path('edit_user_<int:user_id>', views.edit_user, name='edit_user'),
   
   #account setting
   path('settings/', views.account_settings, name='account_settings'),
   path('edit_email_<int:user_id>', views.edit_email, name='edit_email'),
   path('edit_password_<int:user_id>', views.edit_user_psw, name='edit_user_psw'),
   
   #delete user system
   path('delete_account/', views.delete_account, name='delete_account'),
   path('delete_user_<int:user_id>', views.delete_user, name='delete_user'),
   
   #logout user
   path('logout', views.logout_user, name='logout')
]