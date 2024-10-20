from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Маршрут для главной страницы
    path('search/', views.product_search, name='product_search'),  # Маршрут для страницы поиска
]

