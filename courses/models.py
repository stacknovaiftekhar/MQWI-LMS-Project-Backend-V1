from django.db import models
from users.models import Teacher


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255, blank=True)
    short_desc = models.TextField()
    description = models.TextField()
    specialty = models.TextField()
    thumbnail = models.ImageField(upload_to='images/courses/', null=True, blank=True)
    start_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Feature(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='features')
    duration = models.DecimalField(max_digits=3, decimal_places=0)
    session = models.DecimalField(max_digits=2, decimal_places=0)
    enrollment = models.DecimalField(max_digits=6, decimal_places=2)
    tuition = models.DecimalField(max_digits=6, decimal_places=2)    
    gender = models.CharField(max_length=255, blank=True)
    format = models.CharField(max_length=100, blank=True)
    opportunity = models.CharField(max_length=255, blank=True)
    guidance = models.CharField(max_length=255, blank=True)
    revision = models.CharField(max_length=255, blank=True)
    support = models.CharField(max_length=255, blank=True)
    resources = models.CharField(max_length=255, blank=True)
    certificate = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Features of {self.course.title}"

    class Meta:
        verbose_name = "Feature"
        verbose_name_plural = "Features"
        ordering = ["-id"]


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        ordering = ['order']


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    video = models.URLField(blank=True, null=True)
    sheet = models.FileField(upload_to='lessons/sheets/', blank=True, null=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']