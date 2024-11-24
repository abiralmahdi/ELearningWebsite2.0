from django.shortcuts import render

# home page
def home(request):
    return render(request, 'index.html')

# contact page
def contact(request):
    return render(request, 'about.html')

# products list page
def products(request):
    return render(request, 'about.html')

# offers page
def offers(request):
    return render(request, 'about.html')

# individual products page
def indiv_product(request):
    return render(request, 'about.html')
