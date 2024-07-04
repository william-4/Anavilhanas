"""
This module provides various functions that handle the business logic.
They handle api calls from the front end as appropriate.

Functions:
- add: Returns the sum of two numbers.
- subtract: Returns the difference of two numbers.
"""


from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate

from .forms import CustomUserCreationForm, combinedForm, categoriesForm
from .models import Addresses, Categories, Products, Images, Carts, cartItems, Orders
from .mpesa import getAccessToken


def create_product(request):
    if request.method == 'POST':
        form = combinedForm(request.POST, request.FILES)
        if form.is_valid():
            if not Products.objects.filter(name=form.cleaned_data['name']).exists():
                item_exists = False
                product = Products.objects.create(
                    name=form.cleaned_data['name'],
                    category=form.cleaned_data['category'],
                    price=form.cleaned_data['price'],
                    quantity=form.cleaned_data['quantity'],
                    description=form.cleaned_data['description'],
                    features=form.cleaned_data['features']
                )
                Images.objects.create(
                    product=product,
                    image1=form.cleaned_data['image1_url'],
                    image2=form.cleaned_data['image2_url'],
                    image3=form.cleaned_data['image3_url'],
                    image4=form.cleaned_data['image4_url'],
                    image5=form.cleaned_data['image5_url']
                )
                count = Products.objects.count()
                if count:
                    context =  {
                        "form": form,
                        "count": count,
                        "item_exists": item_exists,
                    }
                return render(request, 'shop/create_product.html', context)
            else:
                item_exists = True
                count = Products.objects.count()
                if count:
                    context =  {
                        "form": form,
                        "count": count,
                        "item_exists": item_exists,
                    }
                return render(request, 'shop/create_product.html', context)
    else:
        form = combinedForm()
    return render(request, 'shop/create_product.html', {'form': form})


def create_category(request):
    if request.method == "POST":
        form = categoriesForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            item_exists = False
            if Categories.objects.filter(name=name).exists():
                item_exists = True
                count = Categories.objects.count()
                context = {
                    "form": form,
                    "count": count,
                    "item_exists": item_exists,
                }
                return render(request, 'shop/create_category.html', context)
            else:
                category = form.save()
                count = Categories.objects.count()
                context = {
                    "form": form,
                    "count": count,
                }
                return render(request, 'shop/create_category.html', context)
    else:
        form = categoriesForm()
        count = Categories.objects.count()
        context = {
            "form": form,
            "count": count,
        }
    return render(request, 'shop/create_category.html', context)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('shop:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'shop/register.html', {'form': form})


def home(request):
    return render(request, 'shop/home.html')


def products(request):
    """Returns a json of all the products in the database"""
    products = Products.objects.prefetch_related('images').all()
    products_list = list(products.values())
    if products_list:
        context =  {
            "products": products
        }
        return render(request, "shop/products.html", context)
    else:
        return HttpResponse("No products in the products table")


# Home Page
def popular(request):
    """Returns a json of the popular products from the database"""
    popular = Products.objects.all()[:4]
    popular_list = list(popular.values())
    return JsonResponse(popular_list, safe=False)


def top_categories(request):
    """Returns a json of the top categories from the database"""
    categories = Categories.objects.all()
    categories_list = list(categories)[:4]
    return JsonResponse(categories_list, safe=False)


# Profile Page
def profile(request):
    """Returns a json of the user's profile information and shipping address from the database"""


# Categories Page
def sort(request, parameter):
    """
    Sorts the products in the category according to the specified parameter and returns a json of the sorted items.
    Initially just sort according to alphabetical order.
    """


def categories(request):
    """Returns a json of all categories from the database"""
    categories = Categories.objects.all()
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
        "other_products": others,
    }
    return render(request, "shop/product.html", context)


def add_to_cart(request, product_id):
    """Adds the specific product to the cart"""
    # Check if user_id exists in the cart table. If yes, add item to cart_items table while maintaining the cart_id.
    user = request.user
    cart = None
    try:
        cart = get_object_or_404(Carts, user=user, active=True)
    except:
        cart = Carts.objects.create(user=user, active=True)
        try:
            cart = get_object_or_404(Carts, user=user, active=True)
        except:
            return JsonResponse(f"User {user.id} has refused to create cart", safe=False)

    # Check if product exists in cart and update quantity value else create new cartItem
    try:
        product = get_object_or_404(Products, pk=product_id)
        cart_item = get_object_or_404(cartItems, cart=cart, product=product,)
        cart_item.quantity += 1
    except:
        product = get_object_or_404(Products, pk=product_id)
        cartItems.objects.create(cart=cart, product=product, quantity=1)
    return HttpResponse(f"User {user.id} has a cart of id {cart.id}")


def add_quantity(request, product_id):
    """Add the quantity of the specific product"""
    user = request.user
    cart = None
    cart_item = None
    try:
        cart = get_object_or_404(Carts, user=user, active=True)
    except:
        return JsonResponse(f"User {user.id} has no cart but wants to add quantity", safe=False)

    # Check if product exists in cart and update quantity value else raise an error
    try:
        product = get_object_or_404(Products, pk=product_id)
        cart_item = get_object_or_404(cartItems, cart=cart, product=product)
    except:
        return JsonResponse(f"User {user.id} has no cartItem but wants to add quantity", safe=False)
    if cart_item:
        cart_item.quantity += 1
    return HttpResponse(f"Product {product.id} for User {user.id} has update quantity")


# Cart Page
def cart_detail(request):
    """Returns json of the items in the cart for the specific user"""
    if request.user:
        try:
            # Get the cart for the current user
            cart = get_object_or_404(Carts, user=request.user, active=True)
            # Get all items in the cart
            cart_items = cartItems.objects.filter(cart=cart)
        except Carts.DoesNotExist:
            # Handle the case where the cart does not exist
            return HttpResponse("Cart does not exist")
        context = {
            'cart_items': cart_items,
            'cart_id': cart.id,
        }
        return render(request, "shop/cart.html", context)
    else:
        return HttpResponse("User is not logged in")


def delete(request, product):
    """Deletes a product from the cart"""
    try:
        # Get the cart for the current user
        cart = get_object_or_404(Carts, user=request.user, active=True)
    except Carts.DoesNotExist:
        # Handle the case where the cart does not exist
        return HttpResponse("Cart does not exist")
    cart_item = cartItems.objects.filter(cart=cart, product=product)
    cart_item.delete()
    return HttpResponse(f"Product {product.id} has been deleted from user {request.user.id} cart.")



def shipping_cost(request, user_id):
    """
    Returns the cost of shipping based on the shipping address of the user.
    If no shipping address, indicate a dash to be filled in the checkout page
    """

def total_price(request, cart_id):
    """Calculates total price of the products in the cart inclusive of the shipping cost"""

def checkout(request, cart_id):
    """
    Adds order to order table, maintaining link to user.
    Adds cart items to order table
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


"""
1. Adding product to cart
- Query Carts table for an active cart for the user
- If no active cart exists, create a new cart, mark as active and retrieve the cart_id
- Add the product to cart

2. Updating the Cart
- If item already exists in the cart, update the quantity

3. Viewing the cart
- Query cartItems table to get the products and quantities using the cart_id

4. Checkout Process
- Pull the user's address information from the database if exists and populate in the form
- If no shipping address, leave them blank to be filled. If user chooses to create an account,
    prompt them for their password since we have all the other information.
    --- User has to verify their authenticity to be able to access some features like order history. ---
- Query cartItems table to showcase an overview of the products in the order
- When user taps on make payment, create new order

5. Create Order
- Create a new order for user and populate the orderItems table
- Process payment and update Payments table
- Update payment status for the specific order and proceed to order confirmation page
- Send a confirmation email to the user
- Mark cart as inactive 
"""