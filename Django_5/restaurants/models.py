from django.db import models

# Сначала объявляем модель Specialization
class Specialization(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Затем объявляем модель Restaurant
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)  # ссылаемся на Specialization
    phone = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
