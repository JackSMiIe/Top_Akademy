from django import forms

class ProductSearchForm(forms.Form):
    query = forms.CharField(label='Поиск товара', max_length=100)
