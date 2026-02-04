from django.contrib import admin
from .models import Category, Product

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'nomi', 'narxi', 'omborda_bor', 'category', 'qoshgan_sana')
    list_filter = ('category',)
    search_fields = ('nomi',)
