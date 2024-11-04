from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Book
from .forms import BookForm

def book_list(request):
    books = Book.objects.all()
    paginator = Paginator(books, 3)  # Пагинация по 3 книги на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'books/book_list.html', {'page_obj': page_obj})


@user_passes_test(lambda u: u.is_staff)
def add_book(request):
    return render(request, 'books/add_book.html')


def home(request):
    return render(request, 'books/home.html')

@user_passes_test(lambda u: u.is_staff)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Перенаправление на список книг после успешного добавления
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})