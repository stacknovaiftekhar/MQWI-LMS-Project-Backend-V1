from django.contrib import admin
from .models import Payment, Invoice


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'type', 'amount', 'status')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'payment', 'issued', 'emailed')