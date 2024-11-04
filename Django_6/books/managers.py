# books/managers.py

from django.db import models

class BookManager(models.Manager):
    def even_books(self):
        # Используем Python для фильтрации книг с чётными ID
        return [book for book in self.all() if book.id % 2 == 0]

    def books_by_author(self, author_name):
        return self.filter(author__name__icontains=author_name)