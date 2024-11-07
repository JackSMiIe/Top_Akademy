from django.contrib import admin
from .models import Student, Subject, StudSub

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'get_fio')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('get_subject',)

@admin.register(StudSub)
class StudSubAdmin(admin.ModelAdmin):
    list_display = ('id_stud', 'id_sub', 'grade')
