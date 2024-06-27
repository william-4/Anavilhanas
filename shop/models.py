from django.db import models
from django.contrib.auth.models import User


class shippingAddresses(models.Model):
    user_id = models.IntegerField()
    city = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    estate = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    price = models.IntegerField(default=0)


class Products(models.Model):
    product_name = models.CharField("product", max_length=100)
    product_category = models.CharField("categories", max_length=200)
    product_price = models.IntegerField("price", default=0)
    product_quantity = models.IntegerField("quantity", default=0)
    Product_description = models.CharField("description", max_length=300)
    product_features = models.CharField("features", max_length=300)
    image_1 = models.ImageField(default='default.jpg', blank=True)
    product_created = models.DateTimeField("date_added", auto_now_add=True)
    product_updated = models.DateTimeField("date_updated", auto_now=True)

    def __str__(self):
        return (f"ID: {self.id}, Name: {self.product_name}")


class Cart(models.Model):
    user_id = models.IntegerField()
    cart_created = models.DateTimeField("date_created", auto_now_add=True)
    cart_updated = models.DateTimeField("date_updated", auto_now=True)


class Orders(models.Model):
    user_id = models.IntegerField()
    cart_id = models.IntegerField()
    order_created = models.DateField(auto_now_add=True)
    payment = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)


class Item(models.Model):
    cart_id = models.IntegerField()
    order_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.IntegerField(default=1)
    item_created = models.DateTimeField(auto_now_add=True)


class shippingPrices(models.Model):
    town = models.CharField(max_length=100)
    estate = models.CharField(max_length=100)
    price = models.IntegerField(default=0)


# Rationale - Every user can only have one cart. Once payment is confirmed, cart_id is deleted from cart table and order is created for the user.
# Check on the cascade functionality. When cart is deleted from cart table it should not affect the tables linked to it.

# Cart View - shows the user id, cart id and cart items
# select cart_items where cart items cart_id == cart_id

# Orders View - shows the user id, order it and order items
# select cart_id where order_id == order_id, select cart_items where cart_id == cart_id
