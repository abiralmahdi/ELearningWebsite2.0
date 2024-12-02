"""
ShopEasy E Commerce Website
------------------------------
Author: Abir, Tamim, Saidul
Date: 2024-12-02
------------------------------
Description:
This is the views.py file for the home app.
This file contains the following views:
    - home: This view is used to render the home page.
    - contact: This view is used to render the contact page.
    - offers: This view is used to render the offers page.
    - offers_per_category: This view is used to render the offers page for each category.
    - products_page: This view is used to render the products list page.
    - indiv_product: This view is used to render the individual products page.
    - add_to_cart: This view is used to add a product to the cart of a specific user.
    - generate_random_code: This function is used to generate a random character code.
    - checkout: This function is used to checkout the items in the cart.
    - trigger_checkout: This view is used to trigger the checkout process.
    - successful_transanction: This view is used to handle successful transactions.
    - failed_transanction: This view is used to handle failed transactions.
------------------------------
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required
import requests
import random
import string
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


# home page
@csrf_exempt
def home(request):
    """
    This view is used to render the home page.
    It fetches all the categories and offers from the database.
    It also fetches the cart items of the user and calculates the total price of the items in the cart.
    """
    categories = Categories.objects.all() # Fetching all the categories
    offers = Offers.objects.all() # Fetching all the offers
    cart_items = Cart.objects.filter(user=request.user)
    # calculate the total price of the items in cart
    price = 0
    for item in cart_items:
        price = price + item.product.price*item.quantity
    print(price)

    return render(request, 'index.html', {"categories":categories, "offers":offers, "cart_items":cart_items, "price":price})

# contact page
def contact(request):
    """
    This view is used to render the contact page.
    It fetches the cart items of the user and calculates the total price of the items in the cart.
    It also handles the form submission and saves the contact details in the database.
    """
    if request.method =='POST':
        name = request.POST['name']
        message = request.POST['message']
        email = request.POST['email']
        Contact.objects.create(name=name, email=email, message=message)
        return redirect("/")
    cart_items = Cart.objects.filter(user=request.user)
    price = 0
    for item in cart_items:
        price = price + item.product.price*item.quantity
    return render(request, 'contact.html',{"cart_items":cart_items, "price":price})

# offers page
def offers(request):
    """
    This view is used to render the offers page.
    It fetches all the offers from the database.
    It also fetches the cart items of the user and calculates the total price of the items in the cart.
    """
    offers = Offers.objects.all() # Fetching all the offers
    cart_items = Cart.objects.filter(user=request.user)
    price = 0
    for item in cart_items:
        price = price + item.product.price*item.quantity
    return render(request, 'offers.html', {"offers": offers, "cart_items":cart_items, "price":price})


# offers page for each category
def offers_per_category(request, category):
    """
    This view is used to render the offers page for each category.
    It fetches all the products of a specific category from the database.
    It also fetches the cart items of the user and calculates the total price of the items in the cart.
    """
    cart_items = Cart.objects.filter(user=request.user)
    price = 0
    for item in cart_items:
        price = price + item.product.price*item.quantity
    products = Products.objects.filter(category=category) # fetching all the products of a category
    offers_array = []
    for product in products:
        if Offers.objects.get(product=product).exists():
            offers_array.append(Offers.objects.get(product=product))

    discountedPrices = [] # Storing the discounted prices
    for offer in offers_array:
        discount = offer.discount
        product = offer.product
        price = product.price
        discountedPrice = price - (price * discount / 100) # Calculating the discounted price
        discountedPrices.append(discountedPrice)
    
    return render(request, 'offers.html', {"offers": offers_array, "cart_items":cart_items, "price":price})


# products list page
def products_page(request, category):
    """
    This view is used to display the products of a specific category
    It fetches all the products of a specific category from the database.
    It also fetches the cart items of the user and calculates the total price of the items in the cart.

    """
    products = Products.objects.filter(category=category) # Fetching all the products in tge specific category
    cart_items = Cart.objects.filter(user=request.user)
    price = 0
    for item in cart_items:
        price = price + item.product.price*item.quantity
    return render(request, 'products.html', {"products":products, "cart_items":cart_items, "price":price})

# individual products page
def indiv_product(request, category, product):
    """
    This view is used to display the individual product page.
    It fetches the product matching with the relevant id from the database.
    It also fetches the cart items of the user and calculates the total price of the items in the cart.
    """
    product_ = Products.objects.get(id=product) # Fetching the product matching with the relevant id
    cart_items = Cart.objects.filter(user=request.user)
    price = 0
    for item in cart_items:
        price = price + item.product.price*item.quantity
    if Cart.objects.filter(product=product_, user=request.user).exists():
        in_cart = True
    else:
        in_cart = False
    return render(request, 'indiv_product.html', {"product":product_, "in_cart":in_cart, "cart_items":cart_items, "price":price})



# Adds a product to the cart of a specific user
@login_required
def add_to_cart(request, product, qty):
    """
    This view is used to add a product to the cart of a specific user.
    It fetches the product matching with the relevant id from the database.
    It also fetches the cart items of the user and calculates the total price of the items in the cart.
    """
    cart_items = Cart.objects.filter(user=request.user) # fetch all the cart items
    # count the total price of all the items in the cart
    price = 0
    for item in cart_items: # iterate over each items in cart and get the prices
        price = price + item.product.price*item.quantity

    quantity = qty
    user = request.user
    product = Products.objects.get(id=product)

    cart = Cart(product=product, quantity=quantity, user=user) # save the items in the cart
    cart.save()
    # if user has already a cart, return to the previous url  
    if Cart.objects.filter(product=product, user=user).exists():
        return redirect("/category/"+str(product.category.id)+"/"+str(product.id))
    return redirect("/category/"+str(product.category.id)+"/"+str(product.id))


# Generates random character code
def generate_random_code(length=8):
    """
    This function is used to generate a random character code.
    """
    # Choose from uppercase letters, lowercase letters, and digits
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@csrf_exempt
def checkout(amount, trans_id, user_id):
    """
    This function is used to checkout the items in the cart.
    It makes a POST request to the online payment gateway API.
    """
    # API endpoint
    url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"

    # Parameters for the POST request
    data = {
        "store_id": "abira67457d735b0e8",
        "store_passwd": "abira67457d735b0e8@ssl",
        "total_amount": amount,
        "currency": "BDT",
        "tran_id": trans_id,
        "success_url": "http://127.0.0.1:8000/success/"+str(user_id),
        "fail_url": "http://127.0.0.1:8000/fail/",
        "cancel_url": "http://127.0.0.1:8000/cancel/",
        "cus_name": "Customer Name",
        "cus_email": "cust@yahoo.com",
        "cus_add1": "Dhaka",
        "cus_add2": "Dhaka",
        "cus_city": "Dhaka",
        "cus_state": "Dhaka",
        "cus_postcode": "1000",
        "cus_country": "Bangladesh",
        "cus_phone": "01711111111",
        "cus_fax": "01711111111",
        "shipping_method":"NO",
        "product_name": "ABC",
        "product_category": "ABC",
        "product_profile": "general"
    }

    # Make the POST request
    try:
        response = requests.post(url, data=data)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse and handle the response
            print("Response Status:", response.status_code)
            print("Response Data:", response.json())  # Assumes the response is in JSON format
            return response.json()
        else:
            print("Request Failed:", response.status_code)
            print("Response Content:", response.text)

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

# Redirects to the online payment gateway url
@csrf_exempt
def trigger_checkout(request, amount):
    """
    This view is used to trigger the checkout process.
    It fetches the cart items of the user and calculates the total price of the items in the cart.
    """
    cart_items = Cart.objects.filter(user=request.user)
    cart_items =  list(cart_items )
    cart_list = [items.product.name for items in cart_items]
    transanction = Transanction.objects.create(user=request.user.username, amount=int(float(amount)), date=datetime.today())
    transanction.items['data'] = cart_list
    transanction.save()
    response = checkout(int(float(amount)), transanction.id, request.user.id)
    return redirect(response['redirectGatewayURL'])

@csrf_exempt
def successful_transanction(request, user_id):
    """
    This view is used to handle successful transactions.
    It fetches the cart items of the user and calculates the total price of the items in the cart.
    """
    user = User.objects.get(id=int(user_id))
    cart_items = Cart.objects.filter(user=user)
    for item in cart_items:
        item.delete()
    return redirect("/")

@csrf_exempt
def failed_transanction(request):
    """
    This view is used to handle failed transactions.
    """
    return JsonResponse({"status": "Transanctions failed. Please try again some other time."})