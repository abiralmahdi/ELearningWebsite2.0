from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login, name='home'),
    path('register', views.register, name='about'),
]