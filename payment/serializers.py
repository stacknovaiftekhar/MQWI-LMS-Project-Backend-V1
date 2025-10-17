from rest_framework import serializers
from .models import Payment, Invoice
from contact.models import WalletInfo, BankDetail


class PaymentSerializer(serializers.ModelSerializer):
    enrollment_info = serializers.SerializerMethodField()
    payment_method = serializers.SerializerMethodField()    
    invoice = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            'id', 'enrollment', 'type', 'amount', 'month',
            'content', 'object', 'txn_id', 'status', 'date',
            'enrollment_info', 'payment_method', 'invoice'
        ]
        read_only_fields = ['date']

    def get_enrollment_info(self, obj):
        return {
            'student': obj.enrollment.student.fullname,
            'course': obj.enrollment.course.title
        }

    def get_payment_method(self, obj):
        if isinstance(obj.method, WalletInfo):
            return f"{obj.method.name} ({obj.method.number})"
        elif isinstance(obj.method, BankDetail):
            return f"{obj.method.bank} ({obj.method.account})"
        return "Unknown"

    def get_invoice(self, obj):
        if hasattr(obj, 'invoice'):
            return {
                'id': obj.invoice.id,
                'number': obj.invoice.number,
                'issued': obj.invoice.issued,
                'emailed': obj.invoice.emailed,
                'pdf_file': obj.invoice.pdf_file.url if obj.invoice.pdf_file else None
            }
        return None


class InvoiceSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    course_title = serializers.SerializerMethodField()
    pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = [
            'id', 'payment', 'number', 'issued',
            'emailed', 'pdf_file', 'pdf_url',
            'student_name', 'course_title'
        ]
        read_only_fields = ['number', 'issued', 'pdf_file', 'emailed']

    def get_student_name(self, obj):
        return obj.payment.enrollment.student.fullname

    def get_course_title(self, obj):
        return obj.payment.enrollment.course.title

    def get_pdf_url(self, obj):
        return obj.pdf_file.url if obj.pdf_file else None