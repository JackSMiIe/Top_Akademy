from django.db import models
from django.contrib.auth.models import User
from .managers import BookManager

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publish_date = models.DateField()

    def __str__(self):
        return self.title


from django.db import models
from .managers import BookManager


class Book(models.Model):
    title = models.CharField(max_length=200)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    publish_date = models.DateField()

    # Стандартный менеджер Django
    objects = models.Manager()

    # Пользовательский менеджер с дополнительными методами
    booksManager = BookManager()

    def __str__(self):
        return self.title
