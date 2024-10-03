"""
This module provides various functions that handle the business logic.
They handle api calls from the front end as appropriate.

Functions:
- add: Returns the sum of two numbers.
- subtract: Returns the difference of two numbers.
"""
import itertools

from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
import uuid
import requests
import base64
from datetime import datetime

from .forms import customUserCreationForm, customUserEditForm, combinedForm, categoriesForm, addressesForm
from .models import Addresses, Categories, Products, Images, Carts, cartItems, Orders, orderItems, customUser
from .mpesa import getAccessToken
from .mpesa import initiate_stk_push, process_stk_callback

def profile(request):
    if not request.user.is_authenticated:
        return redirect('shop:register')  # Redirect if the user is not authenticated

    user = request.user

    if (user.first_name == user.last_name) and (user.email == user.phone_number):  # Redirect if the user is a temporary user
        return redirect('shop:register')

    # Handle the user's address
    try:
        address = Addresses.objects.get(user=user)
    except Addresses.DoesNotExist:
        address = None

    if request.method == 'POST':
        print(request.POST)
        form1 = customUserEditForm(request.POST, instance=user, prefix='profile')
        form2 = addressesForm(request.POST, instance=address, prefix='address')

        if form1.is_valid():
            form1.save()
        else:
            print(form1.errors)

        if form2.is_valid():
            address_instance = form2.save(commit=False)
            address_instance.user = user
            address_instance.save()
        else:
            print(form2.errors)
        return redirect('shop:profile')  # Redirect after saving
    else:
        form1 = customUserEditForm(instance=user, prefix='profile')
        form2 = addressesForm(instance=address, prefix='address')

        context = {
            "form1": form1,
            "form2": form2,
            "date_field": user.date_of_birth.strftime('%Y-%m-%d') if user.date_of_birth else '',

        }
    return render(request, 'shop/profile.html', context)
    
def register(request):  # Needs to be updated to cater for temporary user who creates an account
    if request.method == 'POST':
        user = request.user

    form = customUserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        email = form.cleaned_data.get('email')
        username = customUser.objects.get(email=email).username
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('shop:profile')
        else:
            return HttpResponse("Invalid credentials")
    else:
        form = customUserCreationForm()
        return render(request, 'shop/register.html', {'form': form})

def test(request):
    return render(request, 'shop/test.html')

def home(request):
    return render(request, 'shop/home.html')

def affiliate(request):
    return render(request, 'shop/affiliate.html')

def products(request, category_id=None):
    categories = Categories.objects.all()
    if category_id is not None:
        category_products = Products.objects.filter(category_id=category_id).order_by('created_at')
    else:
        category_products = Products.objects.filter(category=categories[0]).order_by('created_at')
    
    paginator = Paginator(category_products, 9)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        "categories": categories,
        "products": products,
    }
    return render(request, 'shop/products.html', context=context)

def category(request, category_id):
    """Returns a json of all categories from the database"""
    categories = Categories.objects.all()
    category = Categories.objects.get(id=category_id)
    # categories_list = list(categories)
    category_products = Products.objects.filter(category=category)
    paginator = Paginator(category_products, 9)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        "categories": categories,
        "products": products,
    }
    return render(request, 'shop/products.html', context=context)

# Product Page
def product(request, product_id):
    """
    Get the current user. If guest user, create a guest account for them for the session.
    Fetch the product and the other products to be displayed.
    Fetch cart is user has a cart and fetch the cart_item if it is in the cart.
    If item exists in the cart, update context objects: quantity and in_cart
    """
    if request.user.is_authenticated:
        user = request.user
    else:
        data = str(uuid.uuid4())
        username = f"User-{data}"
        user = customUser.objects.create_user(username=username, password=data, first_name=data, last_name=data, phone_number=data, email=data, city=data)
        user = authenticate(username=username, password=data)
        if user == None:
            return HttpResponse("Error in authentication")
        login(request, user)

    product = get_object_or_404(Products, pk=product_id)
    others = Products.objects.all()[:4]
    context = {
        "product": product,
        "other_products": others,
        "in_cart": "False",
        "quantity": 1
    }
    try:
        cart = Carts.objects.get(user=user, active=True)
    except Carts.DoesNotExist:
        return render(request, "shop/product.html", context)
    try:
        item = cartItems.objects.get(cart=cart, product=product)
    except:
        return render(request, "shop/product.html", context)
    if item:
        context["quantity"] = item.quantity
        context["in_cart"] = "True"
    return render(request, "shop/product.html", context)

def cart(request):
    if request.user.is_authenticated:
        print("request.user is authenticated")
        try:
            # Get the cart for the current user
            cart = get_object_or_404(Carts, user=request.user, active=True)
        except:
            context = {
                "message": "No items in cart"
            }
            return render(request, "shop/cart.html", context)
        try:
            # Get all items in the cart
            cart_items = cartItems.objects.filter(cart=cart)
        except cartItems.DoesNotExist:
            # Handle the case where the cart does not exist
            context = {
                "message": "No items in cart"
            }
            return render(request, "shop/cart.html", context)
        cart_items_with_totals = []
        for item in cart_items:
            total_price = item.product.price * item.quantity
            cart_items_with_totals.append({
                'item': item,
                'total_price': total_price
            })
        context = {
            'cart_items_with_totals': cart_items_with_totals,
            'cart_id': cart.id,
        }
        if len(cart_items_with_totals) == 0:
            context["message"] = "No items in cart"
        return render(request, "shop/cart.html", context)
    else:
        context = {
            "message": "No items in cart"
        }
        return render(request, "shop/cart.html", context)

# Create a temporary user on addition of a product to cart or view of cart
def add_to_cart(request, product_id):
    """Adds the specific product to the cart"""
    # Check if user_id exists in the cart table. If yes, add item to cart_items table while maintaining the cart_id.
    if request.method == 'POST':
        user = request.user
        try:
            product = Products.objects.get(id=product_id)
            # Check if the product is already in the cart
            cart, cart_created = Carts.objects.get_or_create(user=user, active=True, defaults={'user': user, 'active': True})
            item, item_created = cartItems.objects.get_or_create(cart=cart, product=product, defaults={'cart': cart, 'product': product})
            if not item_created:
                return JsonResponse({'status': 'success'})
            item.save()
            return JsonResponse({'status': 'success'})
        except Products.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Product not found'}, status=404)
    return JsonResponse({'status': 'fail', 'message': 'Invalid request method'}, status=400)


def add_quantity(request, product_id):
    """
    Fetch the product from the products table.
    Fetch the cart if it exists and the cart item if already in cart.
    If item is in cart, increase quantity, else add the item in cart and increase quantity
    """
    if request.method == 'POST':
        product = Products.objects.get(id=product_id)
        # Check if the product is already in the cart
        cart, cart_created = Carts.objects.get_or_create(user=request.user, active=True, defaults={'user': request.user, 'active': True})
        item, item_created = cartItems.objects.get_or_create(cart=cart, product=product, defaults={'cart': cart, 'product': product, 'quantity': 1})
        item.quantity += 1
        item.save()
        added = add_to_cart(request, product_id)
        return JsonResponse({'success': True, 'new_quantity': item.quantity})           
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def subtract_quantity(request, product_id):
    """Add the quantity of the specific product"""
    if request.method == 'POST':
        product = Products.objects.get(id=product_id)
        # Check if the product is already in the cart
        cart, cart_created = Carts.objects.get_or_create(user=request.user, active=True, defaults={'user': request.user, 'active': True})
        item, item_created = cartItems.objects.get_or_create(cart=cart, product=product, defaults={'cart': cart, 'product': product, 'quantity': 1})
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
            added = add_to_cart(request, product_id)
            return JsonResponse({'success': True, 'new_quantity': item.quantity})
        return JsonResponse({'success': False, 'error': 'Quantity cannot be less than 1'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def remove_from_cart(request, product_id):
    """Deletes a product from the cart in the product page"""
    product = Products.objects.filter(id=product_id).first()
    try:
        # Get the cart for the current user
        cart = get_object_or_404(Carts, user=request.user, active=True)
    except Carts.DoesNotExist:
        # Handle the case where the cart does not exist
        return HttpResponse("Cart does not exist")
    cart_item = cartItems.objects.filter(cart=cart, product=product)
    cart_item.delete()
    return JsonResponse({'success': True})

def remove(request, product_id):
    """Deletes a product from the cart in the cart page"""
    product = Products.objects.filter(id=product_id).first()
    if not product:
        return JsonResponse({'success': False, 'message': 'Product does not exist'})
    
    try:
        # Get the cart for the current user
        cart = get_object_or_404(Carts, user=request.user, active=True)
    except Carts.DoesNotExist:
        # Handle the case where the cart does not exist
        return JsonResponse({'success': False, 'message': 'Cart does not exist'})
    
    # Find and delete the cart item
    cart_item = cartItems.objects.filter(cart=cart, product=product)
    if not cart_item.exists():
        return JsonResponse({'success': False, 'message': 'Item not found in cart'})
    
    cart_item.delete()
    
    return JsonResponse({'success': True})

def order_confirmation(request):
    return render(request, "shop/order_confirmation.html", )

def checkout(request):
    """
    Adds order to order table, maintaining link to user.
    Adds cart items to order table
    Returns checkout page
    """
    if request.user.is_authenticated:
        try:
            # Get the cart for the current user
            cart = get_object_or_404(Carts, user=request.user, active=True)
            cart_total = cart.get_cart_total()
        except Carts.DoesNotExist:
            return HttpResponse ("Cart does not exist")
            # Get all items in the cart
        try:
            if cart:
                cart_items = cartItems.objects.filter(cart=cart)
        except:
            # Handle the case where the cart does not exist
            return HttpResponse("Cart does not exist")
        context = {
            'cart_items': cart_items,
            'cart_id': cart.id,
            'cart_total': cart_total["total"],
            "items": cart_total["items"]
        }
        return render(request, "shop/checkout.html", context)
    else:
        return HttpResponse("User is not logged in")

def order_confirmatio(request):
    user = request.user
    cart = None

    user_data = model_to_dict(user, fields=['id', 'username', 'email'])

    try:
        cart = get_object_or_404(Carts, user=user, active=True)
    except Carts.DoesNotExist:
        return HttpResponse ("Cart does not exists")

    context = {
        "user": user_data,
        "cart": cart
    }
    return JsonResponse ({"context": context})

# Order Confirmation Page
def order_confirmation(request):
    """Returns order details and profile details"""
    # ideally make payment and only if successful should I proceed to adding items to order tables
    # add cart items to order tables
    user = request.user
    cart = None
    try:
        cart = get_object_or_404(Carts, user=user, active=True)
    except Carts.DoesNotExist:
        return HttpResponse ("Cart does not exists")

    if cart:
        try:
            cart_items = cartItems.objects.filter(cart=cart)
            total = cart.get_cart_total()
        except cartItems.DoesNotExist:
            return HttpResponse("Cart does not exists")

    try:
        address = get_object_or_404(Addresses, user=user)
    except Addresses.DoesNotExist:
        return HttpResponse("User has no address yet")

    shipping_cost = 100

    order = Orders.objects.create(
        user=user,
        address=address,
        shipping_cost=shipping_cost,
        total_amount=total,
        status="payment complete"
    )

    for item in cart_items:
        if item.product:
            # Create an order item for each cart item
            order_item = orderItems.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price  # Store the price at the time of the order
            )

    cart.active = False
    cart.save()

    order_items = orderItems.objects.filter(user=user, order=order)
    context = {
        "order_items": order_items,
        "address": address
    }
    return JsonResponse({"context": "context"})

def place_order(request, cart_id):
    if cart_id:
        # Calculate total amount
        cart = get_object_or_404(Carts, user=request.user, active=True)  # mark cart as inactive when payment is made

        cart_total = cart.get_cart_total()
        # make call to the stk push api with the necessary details and callback function
        context = {
            "cart_total": cart_total,
            "cart_id": cart_id,
        }
        return HttpResponse(context.items())
    else:
        return HttpResponse("Wrong cart id")


def get_access_token():
    consumer_key = 'j25bJmuRY0zWWgpKGwXAVI544bbRYlhku53721OAmiuCBLsG'
    consumer_secret = '5uDG8qv6dsD7g0g1PmRo24UbMiP9IzQNkF2W9XbQzjLnEAFrjfL3CIC8DCB2TBig'
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    response = requests.get(api_url, auth=(consumer_key, consumer_secret))
    json_response = response.json()
    access_token = json_response['access_token']
    print("Access token")
    print(access_token)
    print("response")
    print(json_response)
    return access_token


def stk_push(request, context):
    access_token = get_access_token()
    print("Access token 2")
    print(access_token)

    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # M-Pesa API details
    shortcode = '174379'
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = f"{shortcode}{passkey}{timestamp}"
    password = base64.b64encode(data_to_encode.encode()).decode('utf-8')
    party_A = '254718372119'

    payload = {
        'BusinessShortCode': shortcode,
        'Password': password,
        'Timestamp': timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': 1,  # Context['total']
        'PartyA': party_A,  # Context['phone_number']
        'PartyB': shortcode,
        'PhoneNumber': party_A,  # Context['phone_number']
        'CallBackURL': 'https://e191-105-163-2-247.ngrok-free.app/stk_push_callback/',  # Ngrok or live server URL
        'AccountReference': 'cart sample',  # Context['cart_id']
        'TransactionDesc': 'Payment for cart sample'
    }

    response = requests.post(api_url, json=payload, headers=headers)
    print("response", response)
    response_data = response.json()
    print("response_data when calling the stk push api in stk_push view", response_data)
    
    return (response_data)


def stk_push_callback(request):
    """
    Takes the response from safaricom and the cart id
    """
    # If successful, move items from cart to order and update the database. Return the order confirmation page
    # If unsuccessful, reload the checkout page and alert user that the payment failed and that they should retry
    if request.method == 'POST':
        mpesa_response = request.body.decode('utf-8')
        # Process the response here (e.g., save transaction details in the database)
        print("Response sent to the callback function")
        print(mpesa_response)  # You can parse this response and save to DB
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted", "mpesa_response": mpesa_response})