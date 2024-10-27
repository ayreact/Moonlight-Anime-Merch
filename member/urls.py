from . import views
from django.urls import path
from django.contrib.auth import views as auth_view

urlpatterns = [
   path('sign-up/',views.sign, name='sign'),
   path('log-in/',views.log, name='log'),
   
   #password reset
   path('reset_password/', auth_view.PasswordResetView.as_view(), name='reset_password'),
   path('reset_password_sent/', auth_view.PasswordResetDoneView.as_view(), name='password_reset_done'),
   path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   path('reset_password_complete/', auth_view.PasswordResetCompleteView.as_view(), name='password_reset_complete')
]