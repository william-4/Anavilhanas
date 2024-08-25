""" Module defining the database schema for the online shop application """


from django.db import models
from django.contrib.auth.models import AbstractUser

class customUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        # Update username based on email and first_name
        if not self.username:
            self.username = self.email.split('@')[0] + '_' + self.first_name.lower()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.username


class Addresses(models.Model):
    user = models.ForeignKey('shop.customUser', on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    major_road = models.CharField(max_length=100)
    estate = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Categories(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    description = models.CharField(max_length=300)
    features = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Images(models.Model):
    product = models.OneToOneField(Products, related_name='images', on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='products/images/')
    image2 = models.ImageField(upload_to='products/images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='products/images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='products/images/', blank=True, null=True)
    image5 = models.ImageField(upload_to='products/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Carts(models.Model):
    user = models.ForeignKey('shop.customUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)


class cartItems(models.Model):
    cart = models.ForeignKey(Carts, on_delete=models.PROTECT)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)  # I should not loose the cart item on deletion of a product. Code has to be improved
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Orders(models.Model):
    user = models.ForeignKey('shop.customUser', on_delete=models.CASCADE)
    address = models.ForeignKey(Addresses, on_delete=models.PROTECT)
    shipping_cost = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class orderItems(models.Model):
    order = models.ForeignKey(Carts, on_delete=models.PROTECT)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)  # I should not loose the cart item on deletion of a product. Code has to be improved
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Payments(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.PROTECT)
    amount = models.IntegerField()
    payment_method = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class shippingPrices(models.Model):
    town = models.CharField(max_length=100)
    estate = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
