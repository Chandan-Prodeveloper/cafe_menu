"""from django.urls import path
from . import views

urlpatterns = [
    # Customer-facing menu
    path('menu/', views.customer_menu, name='customer_menu'),
    
    # Admin dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Menu items management
    path('admin/menu-items/', views.menu_items_list, name='menu_items_list'),
    path('admin/menu-items/create/', views.create_menu_item, name='create_menu_item'),
    path('admin/menu-items/<int:pk>/edit/', views.edit_menu_item, name='edit_menu_item'),
    path('admin/menu-items/<int:pk>/delete/', views.delete_menu_item, name='delete_menu_item'),
    path('admin/menu-items/<int:pk>/toggle-availability/', views.toggle_availability, name='toggle_availability'),
    
    # Categories management
    path('admin/categories/', views.categories_list, name='categories_list'),
    path('admin/categories/create/', views.create_category, name='create_category'),
    path('admin/categories/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path('admin/categories/<int:pk>/delete/', views.delete_category, name='delete_category'),
]

"""
from django.urls import path
from . import views

urlpatterns = [
    # Customer-facing menu
    path('', views.customer_menu, name='customer_menu'),
    
    # Admin dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
