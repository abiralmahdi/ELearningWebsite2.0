from django.shortcuts import render
from .models import *

# home page
def home(request):
    categories = Categories.objects.all() # Fetching all the categories
    offers = Offers.objects.all() # Fetching all the offers
    discountedPrices = [] # Storing the discounted prices
    for offer in offers:
        discount = offer.discount
        product = offer.product
        price = product.price
        discountedPrice = price - (price * discount / 100) # Calculating the discounted price
        discountedPrices.append(discountedPrice)
    return render(request, 'index.html', {"categories":categories, "offers":offers, "discounts":discountedPrices})

# contact page
def contact(request):
    return render(request, 'contact.html')

# products list page
def products_page(request, category):
    products = Products.objects.filter(category=category) # Fetching all the products in tge specific category
    return render(request, 'products.html', {"products":products})

# offers page
def offers(request):
    return render(request, 'about.html')

# individual products page
def indiv_product(request, category, product):
    product_ = Products.objects.get(id=product) # Fetching the product matching with the relevant id
    return render(request, 'indiv_product.html', {"product":product_})

# Adds products to the DB in a specific category
def addProducts(request, category):
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
def addCategory(request):
    if request.method == "POST": # If the form method is POST
        name = request.POST['name']
        description = request.POST['description']
        image = request.FILES['image']
        category = Categories(name=name, description=description, image=image)
        category.save()
        return render(request, 'addCategory.html', {"message":"Category added successfully"})
    return render(request, 'addCategory.html')

# Adds an Offer to an existing product
def addOffer(request):
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
def addToCart(request, product):
    if request.method == "POST": # If the form method is POST
        quantity = request.POST['quantity']
        user = request.POST['user']
        product = Products.objects.get(id=product)
        cart = Cart(product=product, quantity=quantity, user=user)
        cart.save()
        return render(request, 'addToCart.html', {"message":"Product added to cart successfully"})
    return render(request, 'addToCart.html')