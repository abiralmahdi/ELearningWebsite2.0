from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('category/<str:category>/', views.products_page, name='productsPage'),
    path('category/<str:category>/<str:product>', views.indiv_product, name='indiv_product'),
]