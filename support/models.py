from django.db import models


class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    mobile = models.CharField(max_length=20)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    replied = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name