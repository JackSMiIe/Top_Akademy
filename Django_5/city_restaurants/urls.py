from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Функция для перенаправления с главной страницы
def home_redirect(request):
    return redirect('search_restaurants')  # перенаправляем на путь 'search_restaurants'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('restaurants/', include('restaurants.urls')),  # подключение маршрутов приложения
    path('', home_redirect, name='home'),  # перенаправление с главной страницы
]

