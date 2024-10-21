from django import forms
from .models import Customer, Seller, Product, Sale

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'email']

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['first_name', 'last_name', 'phone', 'email', 'hire_date', 'position']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'seller', 'product', 'sale_date', 'sale_amount']
