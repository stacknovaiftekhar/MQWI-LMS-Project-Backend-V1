from django.db import models
from users.models import Student
from courses.models import Course, Module, Lesson


class Enrollment(models.Model):
    STATUS_CHOICES = [ ('Pending', 'Pending'), ('Enrolled', 'Enrolled'), ('Cancelled', 'Cancelled'), ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.fullname} -> {self.course.title}"

    class Meta:
        unique_together = ('student', 'course')


class LessonProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progress')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'lesson')  # Prevent duplicate tracking


class ModuleProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='module_progress')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='user_progress')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'module')