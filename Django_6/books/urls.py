# books/urls.py
from django.urls import path
from . import views
from .views import BookListCreateAPIView, BookRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', views.book_list, name='book_list'),  # Список книг
    path('add/', views.add_book, name='add_book'),  # Добавить книгу
    path('authors/', views.author_list, name='author_list'),  # Список авторов

    # API маршруты
    path('api/books/', BookListCreateAPIView.as_view(), name='book-list-create'),  # API для списка книг и создания
    path('api/books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book-retrieve-update-destroy'),  # API для просмотра, обновления и удаления книги
    path('test-exception/', views.test_exception, name='test_exception'),
]
