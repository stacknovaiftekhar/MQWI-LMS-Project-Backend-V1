from django.contrib import admin
from .models import Category, Course, Feature, Module, Lesson


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_teacher_name', 'category')
    list_filter = ('category', )
    search_fields = ('title', 'teacher__fullname', 'category__name')

    def get_teacher_name(self, obj):
        return obj.teacher.fullname
    get_teacher_name.short_description = 'Teacher Name'


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('course', 'duration', 'tuition')
    list_filter = ('gender', )
    search_fields = ('course__title',)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'title', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    ordering = ('order',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'module', 'title', 'video')
    list_filter = ('module',)
    search_fields = ('title', 'module__title')