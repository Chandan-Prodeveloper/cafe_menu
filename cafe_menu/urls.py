"""from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('menu.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from menu import views as menu_views

urlpatterns = [
    # Custom admin panel (must come before Django admin to take priority)
    path('admin/menu-items/', menu_views.menu_items_list, name='menu_items_list'),
    path('admin/menu-items/create/', menu_views.create_menu_item, name='create_menu_item'),
    path('admin/menu-items/<int:pk>/edit/', menu_views.edit_menu_item, name='edit_menu_item'),
    path('admin/menu-items/<int:pk>/delete/', menu_views.delete_menu_item, name='delete_menu_item'),
    path('admin/menu-items/<int:pk>/toggle-availability/', menu_views.toggle_availability, name='toggle_availability'),
    path('admin/categories/', menu_views.categories_list, name='categories_list'),
    path('admin/categories/create/', menu_views.create_category, name='create_category'),
    path('admin/categories/<int:pk>/edit/', menu_views.edit_category, name='edit_category'),
    path('admin/categories/<int:pk>/delete/', menu_views.delete_category, name='delete_category'),
    
    # Django admin (comes after custom routes)
    path('admin/', admin.site.urls),
    
    # App URLs
    path('', include('menu.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
