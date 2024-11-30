from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.log_in, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.log_out, name='logout'),
    path('admin_dashboard/add_products/', views.add_products, name='add_products'),
    path('admin_dashboard/add_offers/<str:product>', views.add_offers, name='add_offers'),
    path('admin_dashboard/', views.view_dashboard, name='view_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
]