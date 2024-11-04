from django.contrib import admin
from django.urls import path, include
from books import views as book_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),  # URL для приложения books
    path('', book_views.home, name='home'),  # Корневой URL для стартовой страницы
]

