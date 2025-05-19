from django.contrib import admin
from .models import Category, MenuItem, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display  = ('name', 'price', 'category')
    search_fields = ('name',)
    list_filter   = ('category',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'is_paid', 'created_at')
    list_filter   = ('is_paid', 'created_at')
    search_fields = ('name', 'email')

