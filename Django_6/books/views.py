from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Book, Author
from .forms import BookForm
from rest_framework import generics
from .serializers import BookSerializer



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


class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

def test_exception(request):
    # Представление для тестирования обработки исключений
    return render(request, 'books/non_existent_template.html')

def custom_book_list(request):
    author_name = request.GET.get('author')  # Получаем имя автора из GET-параметра
    even_books = Book.booksManager.even_books()  # Получаем чётные книги

    if author_name:
        books_by_author = Book.booksManager.books_by_author(author_name)
    else:
        books_by_author = None

    return render(request, 'books/custom_book_list.html', {
        'even_books': even_books,
        'books_by_author': books_by_author,
        'author_name': author_name,
    })