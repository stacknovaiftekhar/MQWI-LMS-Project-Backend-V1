from django.db import models


class ContactInfo(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    about = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or "Contact Info"


class SocialLink(models.Model):
    facebook_page = models.URLField(blank=True)
    facebook_group = models.URLField(blank=True)
    whatsapp = models.URLField(blank=True)
    youtube = models.URLField(blank=True)    
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    telegram = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Social Links (id={self.id})"


class WalletInfo(models.Model):
    name = models.CharField(max_length=20)
    number = models.CharField(max_length=20)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Wallet Info"


class BankDetail(models.Model):
    name = models.CharField(max_length=50)
    account = models.CharField(max_length=20)
    bank = models.CharField(max_length=30)
    branch = models.CharField(max_length=30, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Bank Info"