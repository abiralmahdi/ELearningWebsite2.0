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
    categories = Categories.objects.all() # Fetching all the categories
    offers = Offers.objects.all() # Fetching all the offers
    discountedPrices = [] # Storing the discounted prices
    cart_items = Cart.objects.filter(user=request.user)
    # calculate the total price of the items in cart
    price = 0
    for item in cart_items:
        price = price + item.product.price*item.quantity

    for offer in offers:
        discount = offer.discount
        product = offer.product
        price = product.price
        discountedPrice = price - (price * discount / 100) # Calculating the discounted price
        discountedPrices.append(discountedPrice)
    return render(request, 'index.html', {"categories":categories, "offers":offers, "discounts":discountedPrices, "cart_items":cart_items, "price":price})

# contact page
def contact(request):
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
    offers = Offers.objects.all() # Fetching all the offers
    discountedPrices = [] # Storing the discounted prices
    for offer in offers:
        discount = offer.discount
        product = offer.product
        price = product.price
        discountedPrice = price - (price * discount / 100) # Calculating the discounted price
        discountedPrices.append(discountedPrice)
    cart_items = Cart.objects.filter(user=request.user)
    price = 0
    for item in cart_items:
        price = price + item.product.price*item.quantity
    return render(request, 'offers.html', {"offers": offers, "cart_items":cart_items, "price":price})


# offers page for each category
def offers_per_category(request, category):
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
    products = Products.objects.filter(category=category) # Fetching all the products in tge specific category
    cart_items = Cart.objects.filter(user=request.user)
    price = 0
    for item in cart_items:
        price = price + item.product.price*item.quantity
    return render(request, 'products.html', {"products":products, "cart_items":cart_items, "price":price})

# individual products page
def indiv_product(request, category, product):
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

# Adds products to the DB in a specific category
@login_required
def add_products(request, category):
    cart_items = Cart.objects.filter(user=request.user)
    price = 0
    for item in cart_items:
        price = price + item.product.price*item.quantity
    if request.method == "POST": # If the form method is POST
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        discount = request.POST['discount']
        image = request.FILES['image']
        category = Categories.objects.get(name=category) # Fetching the required category where i want to add the product
        # Adding the product in the specific category
        product = Products(name=name, description=description, price=price, discount=discount, category=category, image=image)
        product.save()
        return render(request, 'addProducts.html', {"message":"Product added successfully"})
    return render(request, 'addProducts.html')

# Adds categories to the DB
@login_required
def add_category(request):
    cart_items = Cart.objects.filter(user=request.user)
    price = 0
    for item in cart_items:
        price = price + item.product.price*item.quantity
    if request.method == "POST": # If the form method is POST
        name = request.POST['name']
        description = request.POST['description']
        image = request.FILES['image']
        category = Categories(name=name, description=description, image=image)
        category.save()
        return render(request, 'addCategory.html', {"message":"Category added successfully"})
    return render(request, 'addCategory.html')

# Adds an Offer to an existing product
@login_required
def add_offer(request):
    cart_items = Cart.objects.filter(user=request.user)
    price = 0
    for item in cart_items:
        price = price + item.product.price*item.quantity
    if request.method == "POST": # If the form method is POST
        product = request.POST['product']
        discount = request.POST['discount']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        offer = Offers(product=product, discount=discount, start_date=start_date, end_date=end_date)
        offer.save()
        return render(request, 'addOffer.html', {"message":"Offer added successfully"})
    return render(request, 'addOffer.html')

# Adds a product to the cart of a specific user
@login_required
def add_to_cart(request, product, qty):
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
    # Choose from uppercase letters, lowercase letters, and digits
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@csrf_exempt
def checkout(amount, trans_id, user_id):
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
    cart_items = Cart.objects.filter(user=request.user)
    cart_items =  list(cart_items )
    transanction = Transanction.objects.create(user=request.user, amount=int(float(amount)), date=datetime.today(), items=str(cart_items))
    response = checkout(int(float(amount)), transanction.id, request.user.id)
    return redirect(response['redirectGatewayURL'])

@csrf_exempt
def successful_transanction(request, user_id):
    user = User.objects.get(id=int(user_id))
    cart_items = Cart.objects.filter(user=user)
    for item in cart_items:
        item.delete()
    return redirect("/")

@csrf_exempt
def failed_transanction(request):
    return JsonResponse({"status": "Transanctions failed. Please try again some other time."})