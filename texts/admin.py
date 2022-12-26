from django.contrib import admin
from .models import Recipient, Product, ProductCategory


@admin.register(Recipient)
class RequestDemoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in
                    Recipient._meta.get_fields()]


@admin.register(Product)
class RequestDemoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in
                    Product._meta.get_fields()]


@admin.register(ProductCategory)
class RequestDemoAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'type')  # [field.name for field in
    # ProductCategory._meta.get_fields()]
