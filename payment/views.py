from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from contact.models import WalletInfo, BankDetail
from contact.serializers import WalletInfoSerializer, BankDetailSerializer
from .serializers import PaymentSerializer, InvoiceSerializer
from .permissions import IsOwnerOrReadOnly
from .models import Payment, Invoice
from .services import create_payment_and_enrollment
from .utils import send_invoice_email
import os


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'type', 'month']

    @action(detail=False, methods=['get'], url_path='payment-options')
    def payment_options(self, request):
        wallets = WalletInfo.objects.all()
        banks = BankDetail.objects.all()
        wallet_data = WalletInfoSerializer(wallets, many=True).data
        bank_data = BankDetailSerializer(banks, many=True).data
        return Response({'wallets': wallet_data, 'banks': bank_data})

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset if user.is_staff else self.queryset.filter(enrollment__student__user=user)

        enrollment_id = self.request.query_params.get('enrollment')
        if enrollment_id:
            queryset = queryset.filter(enrollment_id=enrollment_id)

        return queryset

    # 3rd Way:  (Using custom service function)
    def create(self, request, *args, **kwargs):
        try:
            payment = create_payment_and_enrollment(request.data, request.user)
            serializer = self.get_serializer(payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)

    # ACTION: Admin can Verify a Payment, Generate Invoice (if not), and Send Email
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser], url_path='verify')
    def verify_payment(self, request, pk=None):
        payment = self.get_object()
        new_status = request.data.get('status')

        if new_status not in ['Pending', 'Verified']:
            return Response({"detail": "Invalid Status Value!"}, status=status.HTTP_400_BAD_REQUEST)

        # If Verifying Payment
        if new_status == 'Verified':
            if payment.status == 'Verified':
                return Response({"detail": "Payment is Already Verified."}, status=status.HTTP_400_BAD_REQUEST)

            # Mark as Verified
            payment.status = 'Verified'
            payment.save()

            # Generate Invoice if it doesn't Exist
            invoice = getattr(payment, 'invoice', None)
            if not invoice:
                invoice = Invoice.objects.create(payment=payment)
                invoice.generate_pdf()

            # Send Invoice Email
            try:
                send_invoice_email(invoice)
            except Exception as e:
                return Response({"detail": f"Payment Verified but Email Sending Failed: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"detail": "Payment Verified and Invoice Email Sent Successfully."}, status=status.HTTP_200_OK)

        # If Changing to Pending
        elif new_status == 'Pending':
            if payment.status == 'Pending':
                return Response({"detail": "Payment is Already Pending."}, status=status.HTTP_400_BAD_REQUEST)

            # Mark as Pending
            payment.status = 'Pending'
            payment.save()

            # If Invoice Exists, Mark emailed=False
            invoice = getattr(payment, 'invoice', None)
            if invoice:
                invoice.emailed = False
                invoice.save()

            return Response({"detail": "Payment Status set to Pending and Invoice Email Status Reset."}, status=status.HTTP_200_OK)


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['issued']

    def get_queryset(self):
        user = self.request.user
        return self.queryset if user.is_staff else self.queryset.filter(payment__enrollment__student__user=user)

    @action(detail=True, methods=['post'], url_path='send-email')
    def send_invoice_email(self, request, pk=None):
        invoice = self.get_object()

        if invoice.emailed:
            return Response({"detail": "Invoice Already Emailed."}, status=status.HTTP_400_BAD_REQUEST)

        if not invoice.pdf_file:
            return Response({"detail": "Missing PDF File."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from .utils import send_invoice_email  # import at top if needed
            send_invoice_email(invoice)
            return Response({"detail": "Invoice Sent Successfully."}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"detail": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        invoice = self.get_object()
        # Delete associated PDF file
        file_path = invoice.pdf_file.path
        if invoice.pdf_file and os.path.isfile(file_path):
            os.remove(file_path)
        invoice.delete()
        return Response({"message": "Invoice and PDF deleted"}, status=status.HTTP_204_NO_CONTENT)

