from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.template.loader import get_template
from datetime import datetime, date
from django.utils import timezone
from django.db import models
from weasyprint import HTML
from io import BytesIO
import random

from enrolls.models import Enrollment

class Payment(models.Model):
    TYPE_CHOICES = [('Registration', 'Registration Fee'), ('Monthly', 'Monthly Fee'),]
    STATUS_CHOICES = [('Pending', 'Pending'), ('Verified', 'Verified')]

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='payments')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Monthly')
    month = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    content = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object = models.PositiveIntegerField()
    method = GenericForeignKey('content', 'object')
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    txn_id = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.enrollment.student.fullname} - {self.enrollment.course.title} - {self.type}"

    def save(self, *args, **kwargs):
        if self.month:
            if isinstance(self.month, str):
                self.month = datetime.strptime(self.month, "%Y-%m").date()  # Parse YYYY-MM
            if isinstance(self.month, date):
                self.month = self.month.replace(day=1)  # Normalize to First Day
        super().save(*args, **kwargs)


class Invoice(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='invoice')
    number = models.CharField(max_length=20, unique=True, blank=True)
    issued = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='invoices/', null=True, blank=True)
    emailed = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice {self.number} - {self.payment.enrollment.student.fullname}"

    def save(self, *args, **kwargs):
        if not self.number:
            today = timezone.now()
            digits = random.randint(100, 999)
            self.number = f"{today.strftime('%y%m%d')}{digits}"
        super().save(*args, **kwargs)

    def generate_pdf(self):
        template = get_template('payment/invoice_template.html')
        html = template.render({'invoice': self})
        result = BytesIO()
        HTML(string=html).write_pdf(result)
        self.pdf_file.save(f"invoice_{self.number}.pdf", result)