from django.shortcuts import render
from .models import *

# home page
def home(request):
    categories = Categories.objects.all() # Fetching all the categories
    offers = Offers.objects.all() # Fetching all the offers
    return render(request, 'index.html', {"categories":categories, "offers":offers})

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