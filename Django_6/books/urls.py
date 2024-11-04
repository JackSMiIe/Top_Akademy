from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),  # Список книг
    path('add/', views.add_book, name='add_book'),  # Добавить книгу
    path('authors/', views.author_list, name='author_list'),  # Список авторов
]
