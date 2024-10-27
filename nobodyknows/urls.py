from . import views
from django.urls import path

urlpatterns = [
   path('',views.home, name='home'),
   path('about/',views.about, name='about'),
   path('blog/',views.blog, name='blog'),
   path('blog_details/', views.blog_details, name='blog_details'),
   path('contact/',views.contact, name='contact'),
   
   #wa_success system
   path('submit_number', views.wa_group, name='wa_group'),
   path('request_submitted', views.wa_success, name='wa_success')
]