from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required

# home page
def home(request):
    categories = Categories.objects.all() # Fetching all the categories
    offers = Offers.objects.all() # Fetching all the offers
    discountedPrices = [] # Storing the discounted prices
    cart_items = Cart.objects.filter(user=request.user)
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
    cart_items = Cart.objects.filter(user=request.user)
    price = 0
    for item in cart_items:
        price = price + item.product.price*item.quantity
    quantity = qty
    user = request.user
    product = Products.objects.get(id=product)
    cart = Cart(product=product, quantity=quantity, user=user)
    cart.save()
        
    if Cart.objects.filter(product=product, user=user).exists():
        return redirect("/category/"+str(product.category.id)+"/"+str(product.id))
    return redirect("/category/"+str(product.category.id)+"/"+str(product.id))
