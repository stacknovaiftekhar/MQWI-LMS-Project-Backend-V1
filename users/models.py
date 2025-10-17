from django.db import models
from django.contrib.auth.models import User

# Gender choices reused in both models
GENDER_CHOICES = [ ('Male', 'Male'), ('Female', 'Female'), ]

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    fullname = models.CharField(max_length=100)
    name_bn = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    expertise = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    image = models.ImageField(upload_to='images/teachers/', null=True, blank=True, default='images/users/avatar-male.png')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name_plural = "Teachers"


class Student(models.Model):
    Occupations = [ ('Business', 'Business'), ('Service', 'Service'), ('Student', 'Student'), ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    fullname = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    image = models.ImageField(upload_to='images/students/', null=True, blank=True, default='images/users/avatar-male.png')
    occupation = models.CharField(max_length=20, choices=Occupations, blank=True)
    designation = models.CharField(max_length=255, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    facebook = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name_plural = "Students"