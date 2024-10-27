from . import views
from django.urls import path

urlpatterns = [
    #dashboard
    path('', views.dashboard, name='dashboard'),
    #Users
    path('add_member', views.add_member, name='add_member'),
    path('manage_members', views.manage_member, name='manage_member'),
    path('view_member_<int:member_id>', views.view_member, name='view_member'),
    path('delete_user_alt/<int:member_id>', views.delete_member_alt, name='delete_member_alt'),
    path('delete_user/<int:member_id>', views.delete_member, name='delete_member'),
    #Team Members
    path('add_team', views.add_team, name='add_team'),
    path('manage_team', views.manage_team, name='manage_team'),
    path('edit_team_member_<int:team_id>', views.edit_team, name='edit_team'),
    path('delete_team_member_<int:team_id>', views.delete_team_member, name='delete_team_member'),
    path('delete_team', views.delete_team, name='delete_team'),
    #Products
    path('add_product',views.add_product, name='add_product'),
    path('manage_products', views.manage_product, name='manage_product'),
    path('edit_product_<int:product_id>', views.edit_product, name='edit_product'),
    path('delete_product_<int:product_id>', views.delete_product, name='delete_product'),
    path('delete_all_products', views.delete_all_products, name='delete_all_products'),
    #User messages
    path('user_messages', views.user_message, name='user_messages'),
    path('message_detail_<int:message_id>', views.message_detail, name='message_detail'),
    path('delete_message_<int:message_id>', views.delete_message, name='delete_message'),
    path('delete_all_messages', views.delete_all_messages, name='delete_all_messages'),
    #Orders
    path('all_orders', views.all_orders, name='all_orders'),
    path('new_orders', views.new_orders, name='new_orders'),
    path('complete_orders', views.complete_orders, name='complete_orders'),
    path('order_ref', views.order_ref, name='order_ref'),
    path('order_product_<int:product_id>', views.order_product, name='order_product'),
    path('order_detail/<int:order_id>/<int:user_id>', views.order_detail, name='order_detail'),
    path('order_complete/<int:order_id>', views.order_complete, name='order_complete'),
    
    #Blog
    path('new_blog', views.new_blog, name='new_blog'),
    path('manage_blog', views.manage_blog, name='manage_blog'),
    path('edit_blog/<int:blog_id>', views.edit_blog, name='edit_blog'),
    path('delete_blog/<int:blog_id>', views.delete_blog, name='delete_blog'),
    path('delete_all_blog', views.delete_all_blog, name='delete_all_blog'),
    
    #Tasks
    path('task', views.tasks, name='tasks')
]