from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Purpose(models.Model):
    # key = models.SlugField(max_length=50, unique=True, help_text="Unique Identifier (e.g., orphan, zakat)")
    name_en = models.CharField(max_length=100, verbose_name="Purpose (English)")
    name_bn = models.CharField(max_length=100, verbose_name="Purpose (Bangla)")

    def __str__(self):
        return f"{self.name_en} / {self.name_bn}"


class Sadaqah(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    mobile = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=10, choices=[('sadaqah', 'সাদাকাহ'), ('zakat', 'যাকাত')], default='sadaqah')
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE, related_name="purpose")
    content = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object = models.PositiveIntegerField()
    method = GenericForeignKey('content', 'object')
    txn_id = models.CharField(max_length=150, help_text="Transaction ID / Mobile No / Bank Account")
    received = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.purpose.name_en} - ৳{self.amount}"