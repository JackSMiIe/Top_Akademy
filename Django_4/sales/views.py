from django.shortcuts import render, redirect
from .models import Customer, Seller, Product, Sale
from .forms import CustomerForm, SellerForm, ProductForm, SaleForm

# Главная страница (например, можно перенаправить на список покупателей)
def index(request):
    return redirect('customer_list')

# Список покупателей
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'sales/customer_list.html', {'customers': customers})

# Добавление покупателя
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'sales/add_customer.html', {'form': form})

# Список продавцов
def seller_list(request):
    sellers = Seller.objects.all()
    return render(request, 'sales/seller_list.html', {'sellers': sellers})

# Добавление продавца
def add_seller(request):
    if request.method == 'POST':
        form = SellerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('seller_list')
    else:
        form = SellerForm()
    return render(request, 'sales/add_seller.html', {'form': form})

# Список товаров
def product_list(request):
    products = Product.objects.all()
    return render(request, 'sales/product_list.html', {'products': products})

# Добавление товара
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'sales/add_product.html', {'form': form})

# Список продаж
def sale_list(request):
    sales = Sale.objects.all()
    return render(request, 'sales/sale_list.html', {'sales': sales})

# Добавление продажи
def add_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sale_list')
    else:
        form = SaleForm()
    return render(request, 'sales/add_sale.html', {'form': form})
