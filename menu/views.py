from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import MenuItem, Category
from .forms import MenuItemForm, CategoryForm
import qrcode
from io import BytesIO
import base64


def customer_menu(request):
    """Display menu for customers"""
    categories = Category.objects.prefetch_related('items').all()
    
    context = {
        'categories': categories,
        'qr_code': generate_qr_code(request),
    }
    return render(request, 'menu/customer_menu.html', context)


def generate_qr_code(request):
    """Generate QR code for menu URL"""
    menu_url = request.build_absolute_uri('/menu/')
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(menu_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for inline display
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"


@login_required
def admin_dashboard(request):
    """Admin dashboard - overview"""
    stats = {
        'total_items': MenuItem.objects.count(),
        'available_items': MenuItem.objects.filter(is_available=True).count(),
        'total_categories': Category.objects.count(),
        'unavailable_items': MenuItem.objects.filter(is_available=False).count(),
    }
    
    recent_items = MenuItem.objects.select_related('category').order_by('-updated_at')[:5]
    
    context = {
        'stats': stats,
        'recent_items': recent_items,
    }
    return render(request, 'menu/admin/dashboard.html', context)


@login_required
def menu_items_list(request):
    """List all menu items"""
    items = MenuItem.objects.select_related('category').order_by('category', 'name')
    categories = Category.objects.all()
    
    # Filter by category if provided
    category_id = request.GET.get('category')
    if category_id:
        items = items.filter(category_id=category_id)
    
    # Filter by availability if provided
    availability = request.GET.get('availability')
    if availability == 'available':
        items = items.filter(is_available=True)
    elif availability == 'unavailable':
        items = items.filter(is_available=False)
    
    context = {
        'items': items,
        'categories': categories,
        'selected_category': category_id,
    }
    return render(request, 'menu/admin/items_list.html', context)


@login_required
def create_menu_item(request):
    """Create new menu item"""
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item added successfully!')
            return redirect('menu_items_list')
    else:
        form = MenuItemForm()
    
    context = {'form': form, 'title': 'Add New Menu Item'}
    return render(request, 'menu/admin/form.html', context)


@login_required
def edit_menu_item(request, pk):
    """Edit menu item"""
    item = get_object_or_404(MenuItem, pk=pk)
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item updated successfully!')
            return redirect('menu_items_list')
    else:
        form = MenuItemForm(instance=item)
    
    context = {'form': form, 'title': 'Edit Menu Item', 'item': item}
    return render(request, 'menu/admin/form.html', context)


@login_required
def delete_menu_item(request, pk):
    """Delete menu item"""
    item = get_object_or_404(MenuItem, pk=pk)
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Menu item deleted successfully!')
        return redirect('menu_items_list')
    
    context = {'item': item}
    return render(request, 'menu/admin/confirm_delete.html', context)


@login_required
@require_http_methods(["POST"])
def toggle_availability(request, pk):
    """Toggle item availability via AJAX"""
    item = get_object_or_404(MenuItem, pk=pk)
    item.is_available = not item.is_available
    item.save()
    
    return JsonResponse({
        'success': True,
        'is_available': item.is_available,
        'message': f"Item is now {'available' if item.is_available else 'unavailable'}"
    })


@login_required
def categories_list(request):
    """List all categories"""
    categories = Category.objects.annotate(
        item_count=__import__('django.db.models', fromlist=['Count']).Count('items')
    )
    context = {'categories': categories}
    return render(request, 'menu/admin/categories_list.html', context)


@login_required
def create_category(request):
    """Create new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('categories_list')
    else:
        form = CategoryForm()
    
    context = {'form': form, 'title': 'Add New Category'}
    return render(request, 'menu/admin/category_form.html', context)


@login_required
def edit_category(request, pk):
    """Edit category"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('categories_list')
    else:
        form = CategoryForm(instance=category)
    
    context = {'form': form, 'title': 'Edit Category', 'category': category}
    return render(request, 'menu/admin/category_form.html', context)


@login_required
def delete_category(request, pk):
    """Delete category"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('categories_list')
    
    context = {'category': category}
    return render(request, 'menu/admin/confirm_delete.html', context)
