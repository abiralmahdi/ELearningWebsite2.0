from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from home.models import *
from .models import *
import datetime

# Create your views here.

def log_in(request):
    if request.method == 'POST':
        # Fetching the data from the form
        username = request.POST['email']
        password = request.POST['password']
        # Authenticating the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Logging in the user
            login(request, user)
            return redirect("/")
        else:
            return render(request, 'login.html', {"message": "Invalid Credentials"})
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        # Fetching the data from the form
        password = request.POST['password']
        c_password = request.POST['c_password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        # Creating a new user
        if password == c_password:
            user = User.objects.create_user(email, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return redirect("login")
        else:
            return render(request, "register.html", {"message": "Passwords do not match"})
    return render(request, "register.html")

def log_out(request):
    logout(request)
    return redirect("/")

@login_required
def add_products(request):
    if request.user.is_superuser:
        categories = Categories.objects.all()
        if request.method == 'POST':
            # Fetching the data from the form
            name = request.POST['name']
            price = request.POST['price']
            description = request.POST['description']
            category = request.POST['category']
            discount = request.POST['discount']
            discounted_price = float(price) - float(discount)*float(price)/100
            image = request.FILES['img']
            # Creating a new product
            product = Products(name=name, price=price, description=description, discounted_price=discounted_price, category=Categories.objects.get(id=category), discount=discount, image=image)
            product.save()
            
            if discount != "":
                offer = Offers(product=product, discount=discount, start_date=datetime.datetime.now(), end_date=datetime.datetime.now() + datetime.timedelta(days=30))
                offer.save()
            return redirect("/")
        return render(request, "add_products.html", {"category":categories})
    else:
        return HttpResponse("Not an Admin")


@login_required
def add_offers(request, product):
    product_ = Products.objects.get(id=product)
    if request.user.is_superuser:
        if request.method == 'POST':
            discount = request.POST['discount']
            # Creating a new offer
            offer = Offers(product=product_, discount=float(discount), start_date=datetime.datetime.now(), end_date=datetime.datetime.now() + datetime.timedelta(days=30))
            offer.save()
            product_.discounted_price = float(product_.price) - float(discount)*float(product_.price)/100
            product_.discount = float(discount)
            product_.save()
            return redirect("/accounts/admin_dashboard#offers")
        return render(request, "add_offers.html", {"product":product_})
    return render(request, "add_offers.html", {"product":product_})

@login_required
def view_dashboard(request):
    if request.user.is_superuser:
        products = Products.objects.all()
        orders = Transanction.objects.all()
        discounts = Offers.objects.all()
        return render(request, "view-products.html", {"products":products, "orders":orders, "offers":discounts})