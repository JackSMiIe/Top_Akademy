
from django.urls import path
from contacts import views

urlpatterns = [
    path('', views.contact_list, name='contact_list'),  # Список контактов
    path('add/', views.add_contact, name='add_contact'),  # Добавить контакт
    path('edit/<int:contact_id>/', views.edit_contact, name='edit_contact'),  # Редактировать контакт
    path('delete/<int:contact_id>/', views.delete_contact, name='delete_contact'),  # Удалить контакт
]

