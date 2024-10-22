from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant
from .forms import RestaurantForm
from django.core.paginator import Paginator

def edit_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    if request.method == "POST":
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('restaurant_detail', restaurant_id=restaurant.id)
    else:
        form = RestaurantForm(instance=restaurant)

    # Важно, чтобы путь к шаблону включал 'restaurants/'
    return render(request, 'restaurants/edit_restaurant.html', {'form': form, 'restaurant': restaurant})

from django.shortcuts import render
from .models import Restaurant, Specialization

def search_restaurants(request):
    query = request.GET.get('query')  # Получаем запрос из URL
    if query:
        specialization = Specialization.objects.filter(name__icontains=query).first()
        if specialization:
            restaurants = Restaurant.objects.filter(specialization=specialization)
        else:
            restaurants = []
    else:
        restaurants = Restaurant.objects.all()
    return render(request, 'restaurants/search_restaurants.html', {'restaurants': restaurants})

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    return render(request, 'restaurants/restaurant_detail.html', {'restaurant': restaurant})


def all_restaurants(request):
    restaurants_list = Restaurant.objects.all()
    paginator = Paginator(restaurants_list, 5)  # Пагинация по 5 ресторанов на страницу

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'restaurants/all_restaurants.html', {'page_obj': page_obj})