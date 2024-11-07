from django import forms
from .models import Student, Subject, StudSub

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['firstname', 'lastname']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['_subject']

class StudSubForm(forms.ModelForm):
    class Meta:
        model = StudSub
        fields = ['lesson_number', 'lesson_desc', 'id_stud', 'id_sub', 'grade']


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['_subject']  # Поле для названия предмета
        widgets = {
            '_subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название предмета'}),
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = StudSub
        fields = ['lesson_number', 'lesson_desc']
        widgets = {
            'lesson_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Номер урока'}),
            'lesson_desc': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание урока', 'rows': 3}),
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = StudSub
        fields = ['id_stud', 'id_sub', 'grade', 'lesson_number']
        widgets = {
            'id_stud': forms.Select(attrs={'class': 'form-select'}),
            'id_sub': forms.Select(attrs={'class': 'form-select'}),
            'grade': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-select'}),
            'lesson_number': forms.Select(choices=[(i, i) for i in range(1, 11)], attrs={'class': 'form-select'}),
        }
