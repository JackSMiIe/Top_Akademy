from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_student/', views.add_student, name='add_student'),  #добавления студента
    path('student/<int:student_id>/', views.student_info, name='student_info'),


    path('add_subject/', views.add_subject, name='add_subject'),
    path('add_lesson/', views.add_lesson, name='add_lesson'),
    path('add_grade/', views.add_grade, name='add_grade'),
]
