from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .forms import StudentForm, SubjectForm, LessonForm, GradeForm
from .models import StudSub, Student


def home(request):
    records = StudSub.objects.all()
    return render(request, 'good_job/home.html', {'records': records})



def student_info(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    records = StudSub.objects.filter(id_stud=student)
    return render(request, 'good_job/student_info.html', {'student': student, 'records': records})


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = StudentForm()
    return render(request, 'good_job/add_student.html', {'form': form})


def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Предмет успешно добавлен!')
            return redirect('home')
    else:
        form = SubjectForm()
    return render(request, 'good_job/add_subject.html', {'form': form})

def add_lesson(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.grade = 1
            lesson.save()
            return redirect('home')
    else:
        form = LessonForm()
    return render(request, 'good_job/add_lesson.html', {'form': form})

def add_grade(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Оценка успешно добавлена!')
            return redirect('home')
    else:
        form = GradeForm()
    return render(request, 'good_job/add_grade.html', {'form': form})