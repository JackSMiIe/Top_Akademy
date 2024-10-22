from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_restaurants, name='all_restaurants'),  # Показ всех ресторанов
    path('<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('<int:restaurant_id>/edit/', views.edit_restaurant, name='edit_restaurant'),
    path('search/', views.search_restaurants, name='search_restaurants'),
]
