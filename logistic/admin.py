from django.contrib import admin

from logistic.models import Product, Stock


@admin.register(Product)
class CarAdmin(admin.ModelAdmin):
    pass
    # list_display = ['id', 'brand', 'model', 'color']
    # list_filter = ['brand', 'model']


@admin.register(Stock)
class PersonAdmin(admin.ModelAdmin):
    pass

# Register your models here.
