from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Book, Author
from .forms import BookForm

def book_list(request):
    query = request.GET.get('q')  # Получаем значение поискового запроса из GET-параметра
    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query) |  # Поиск по названию книги
            Q(author__name__icontains=query) |  # Поиск по имени автора
            Q(genre__name__icontains=query)  # Поиск по жанру
        )

    paginator = Paginator(books, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'books/book_list.html', {'page_obj': page_obj, 'query': query})


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

def author_list(request):
    authors = Author.objects.all()
    return render(request, 'books/author_list.html', {'authors': authors})