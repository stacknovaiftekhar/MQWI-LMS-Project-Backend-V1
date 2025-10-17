from django.contrib import admin
from .models import Enrollment, LessonProgress, ModuleProgress


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status')


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'completed_at')
    list_filter = ('completed_at', )
    search_fields = ('student__fullname', 'lesson__title')


@admin.register(ModuleProgress)
class ModuleProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'module', 'completed_at')
    list_filter = ('completed_at', )
    search_fields = ('student__fullname', 'module__title')