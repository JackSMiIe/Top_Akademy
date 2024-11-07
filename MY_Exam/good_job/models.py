from django.db import models

class Student(models.Model):
    firstname = models.CharField(max_length=15)
    lastname = models.CharField(max_length=20)

    def get_fio(self):
        return f"{self.lastname} {self.firstname}"

    def __str__(self):
        return self.get_fio()

    class Meta:
        verbose_name_plural = "Студенты" # Изм имя в админке


class Subject(models.Model):
    _subject = models.CharField(max_length=30)

    def get_subject(self):
        return self._subject

    def set_subject(self, new_subject):
        self._subject = new_subject
        self.save()

    def __str__(self):
        return self.get_subject()

    class Meta:
        verbose_name_plural = "Предметы" # Изм имя в админке

class StudSub(models.Model):
    lesson_number = models.PositiveIntegerField()
    lesson_desc = models.TextField()
    id_stud = models.ForeignKey(Student, on_delete=models.CASCADE)
    id_sub = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    def get_avg(self, id_stud, id_sub):
        grades = StudSub.objects.filter(id_stud=id_stud, id_sub=id_sub).values_list('grade', flat=True)
        return sum(grades) / len(grades) if grades else 0

    class Meta:
        verbose_name_plural = "Студенты и Предметы" # Изм имя в админке

