from django.contrib import admin
from .models import Teacher, Student


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'user', 'gender')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'user', 'occupation')