"""
This module provides various functions that handle the business logic.
They handle api calls from the front end as appropriate.

Functions:
- add: Returns the sum of two numbers.
- subtract: Returns the difference of two numbers.
"""


from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Products, Cart, Item, Orders


def index(request):
    return HttpResponse("Hello World. Welcome to Anavilhanas online shopping experience")


class signup(CreateView):
    """Handles account creation"""
    form_class = UserCreationForm
    success_url = reverse_lazy("shop:login")
    template_name = "registration/signup.html"


def products(request):
    """Returns a json of all the products in the database"""
    products = Products.objects.all()
    products_list = list(products.values())
    context =  {
        "products": products_list
    }
    return render(request, "shop/index.html", context)


# Home Page
def popular(request):
    """Returns a json of the popular products from the database"""
    popular = Products.objects.all()[:4]
    popular_list = list(popular.values())
    return JsonResponse(popular_list, safe=False)

def top_categories(request):
    """Returns a json of the top categories from the database"""
    categories = Products.objects.values('product_category').distinct()
    categories_list = list(categories)[:4]
    return JsonResponse(categories_list, safe=False)

def reviews(request):
    """Returns a json of the 3 newest reviews from the database"""


# Profile Page
def profile(request):
    """Returns a json of the user's profile information from the database"""


# Categories Page
def sort(request, parameter):
    """
    Sorts the products in the category according to the specified parameter and returns a json of the sorted items.
    Initially just sort according to alphabetical order.
    """

def categories(request):
    """Returns a json of all categories from the database"""
    categories = Products.objects.values('product_category').distinct()
    categories_list = list(categories)
    return JsonResponse(categories_list, safe=False)

def category(request, category):
    """Returns a json of all products in a specific category from the database"""


# Product Page
def product(request, product_id):
    """Returns json of all information about the specific product and other similar products"""
    product = get_object_or_404(Products, pk=product_id)
    others = Products.objects.all()[:4]
    other_products = list(others.values())
    context = {
        "product": product,
        "other_products": other_products,
    }
    return render(request, "shop/product_page.html", context)

def add_to_cart(request, product_id):
    """Adds the specific product to the cart"""
    # Check if user_id exists in the cart table. If yes, add item to cart_items table while maintaining the cart_id.
    user = request.user

    try:
        cart = get_object_or_404(Cart, user_id=user.id)
    except:
        cart = Cart.objects.create(user_id=user.id)
        try:
            cart = get_object_or_404(Cart, user_id=user.id)
        except:
            return JsonResponse(f"User {user.id} has refused to create cart", safe=False)

    # Check if product exists in cart and update quantity value.
    item = Item.objects.create(cart_id=cart.id, order_id=0, product_id=product_id, quantity=1)
    return JsonResponse(f"User {user.id} has a cart of id {cart.id}", safe=False)


    # If no, create a new cart for the user and persist for subsequent additions.



def add_quantity(request, product_id):
    """Add the quantity of the specific product"""


# Cart Page
def cart_detail(request):
    """Returns json of the items in the cart for the specific user"""
    try:
        # Get the cart for the current user
        cart = get_object_or_404(Cart, user_id=request.user.id)
        # Get all items in the cart
        cart_items = Item.objects.filter(cart_id=cart.id)
    except Cart.DoesNotExist:
        # Handle the case where the cart does not exist
        return JsonResponse("Cart does not exist", safe=False)
    
    context = {
        'cart_items': cart_items,
        'cart_id': cart.id,
    }
    return render(request, "shop/cart_page.html", context)

def add_quantity(request, product_id):
    """Add the quantity of the specific product"""

def delete(request, product_id):
    """Deletes a product from the cart"""

def shipping_cost(request, user_id):
    """
    Returns the cost of shipping based on the shipping address of the user.
    If no shipping address, indicate a dash to be filled in the checkout page
    """

def total_price(request, cart_id):
    """Calculates total price of the products in the cart inclusive of the shipping cost"""

def checkout(request, cart_id):
    """
    Adds cart_id to order table, maintaining link to user.
    Returns checkout page
    """
    return render(request, "shop/checkout_page.html")


# Checkout Page
def profile(request, user_id):
    """Returns information about the specific user"""

def ship_to_different_address(request, user_id):
    """
    Displays previously used shipping address information.
    Prompts the user to enter different shipping address information.
    Save that address, maintaining link to the user.
    """

def create_account(request, account_details):
    """
    Creates an account for the user and prompts them to enter and confirm password.
    Saves shipping address for the particular customer
    Authenticate the user by sending pin to mobile phone
    """

def your_order(request, user_id):
    """Returns information on the items in the cart for the specific user in that session."""

def make_payment(request, user_id, payment_method):
    """
    Redirects user to an external link to make the payment.
    Returns user to checkout page once payment is made and confirmed. Button changes to payment made.
    If payment method is payment on delivery, proceed to order confirmation.
    """

def place_order(request, user_id, cart_id):
    """
    Confirms payment, changes payment boolean to True and proceeds to the next page of order confirmation.
    Sends an email and text to user indicating status.
    If in orders table and delivered is False, this means that it is in progress.
    """


# Order Confirmation Page
def order_confirmation_details(request, order_id):
    """Returns order details and profile details"""

def edit_profile(request, user_id):
    """Takes user to profile page."""

def continue_shopping(request):
    """Takes user to categories page"""

def recommendations_for_you(request, user_id):
    """Returns curated products for the user_id"""


