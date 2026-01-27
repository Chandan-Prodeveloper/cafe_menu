from django.db import models
from django.core.validators import MinValueValidator
from PIL import Image
import os


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    SPICE_CHOICES = [
        ('mild', 'Mild'),
        ('medium', 'Medium'),
        ('spicy', 'Spicy'),
        ('extra_spicy', 'Extra Spicy'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(help_text="Detailed description of the dish")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='menu_items/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    spice_level = models.CharField(max_length=20, choices=SPICE_CHOICES, blank=True)
    is_vegetarian = models.BooleanField(default=False)
    preparation_time = models.IntegerField(help_text="Preparation time in minutes", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    def __str__(self):
        return f"{self.name} - ${self.price}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Optimize image size
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 400 or img.width > 400:
                img.thumbnail((400, 400), Image.Resampling.LANCZOS)
                img.save(self.image.path, quality=85, optimize=True)
