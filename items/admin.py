from django.contrib import admin

from .models import Category, Order, Cart

admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Cart)
