from django.contrib import admin

from .models import Products, Categories, Images, customUser


class ImageInline(admin.StackedInline):
    model = Images
    extra = 0  # Number of extra forms to display
    fields = ('image1', 'image2', 'image3', 'image4', 'image5', 'created_at', 'updated_at')  # Fields to display in the inline form
    readonly_fields = ('created_at', 'updated_at')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity', 'description', 'features', 'created_at', 'updated_at')
    search_fields = ('name', 'category')
    list_filter = ('price', 'quantity', 'category')
    inlines = [ImageInline]
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Products, ProductAdmin)
admin.site.register(Categories)
admin.site.register(customUser)