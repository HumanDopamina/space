from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "stock", "active", "updated_at")
    list_filter = ("active",)
    search_fields = ("name", "description")
    list_editable = ("price", "stock", "active")
