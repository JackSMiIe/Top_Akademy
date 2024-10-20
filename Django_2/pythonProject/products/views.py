from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product
from .forms import ProductSearchForm

def product_search(request):
    form = ProductSearchForm(request.GET or None)
    query = None
    products = Product.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        products = products.filter(name__icontains=query)

    paginator = Paginator(products, 3)  # Выводим по 10 товаров на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/product_search.html', {
        'form': form,
        'query': query,
        'page_obj': page_obj,
    })

def home(request):
    return render(request, 'products/home.html')

