from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница или перенаправление
    path('customers/', views.customer_list, name='customer_list'),  # Список покупателей
    path('customers/add/', views.add_customer, name='add_customer'),  # Добавление покупателя
    path('sellers/', views.seller_list, name='seller_list'),  # Список продавцов
    path('sellers/add/', views.add_seller, name='add_seller'),  # Добавление продавца
    path('products/', views.product_list, name='product_list'),  # Список товаров
    path('products/add/', views.add_product, name='add_product'),  # Добавление товара
    path('sales/', views.sale_list, name='sale_list'),  # Список продаж
    path('sales/add/', views.add_sale, name='add_sale'),  # Добавление продажи
]


