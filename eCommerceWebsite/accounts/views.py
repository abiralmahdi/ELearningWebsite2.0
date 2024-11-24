from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

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
