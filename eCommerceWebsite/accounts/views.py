from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, "register.html")

def logout(request):
    return redirect("")