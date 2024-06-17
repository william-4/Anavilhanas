from django.contrib import admin

from .models import Products, shippingPrices


admin.site.register(Products)
admin.site.register(shippingPrices)

