from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from contact.models import WalletInfo, BankDetail
from contact.serializers import WalletInfoSerializer, BankDetailSerializer
from .models import Purpose, Sadaqah
from .serializers import PurposeSerializer, SadaqahSerializer


class PurposeViewSet(viewsets.ModelViewSet):
    queryset = Purpose.objects.all()
    serializer_class = PurposeSerializer


class SadaqahViewSet(viewsets.ModelViewSet):
    queryset = Sadaqah.objects.all()
    serializer_class = SadaqahSerializer

    @action(detail=False, methods=['get'], url_path='payment-options')
    def payment_options(self, request):
        wallets = WalletInfo.objects.all()
        banks = BankDetail.objects.all()
        wallet_data = WalletInfoSerializer(wallets, many=True).data
        bank_data = BankDetailSerializer(banks, many=True).data
        return Response({'wallets': wallet_data, 'banks': bank_data})

    # 1st Way:  (2nd Way is in PaymentViewSet)
    def create(self, request, *args, **kwargs):
        method = request.data.get("method")  # e.g., "wallet" or "bank"
        object = request.data.get("object")  # ID of WalletInfo or BankDetail

        if method == "wallet":
            content = ContentType.objects.get(app_label="contact", model="walletinfo")
        elif method == "bank":
            content = ContentType.objects.get(app_label="contact", model="bankdetail")
        else:
            return Response({"detail": "Invalid Method"}, status=status.HTTP_400_BAD_REQUEST)

        mutable_data = request.data.copy()
        mutable_data["content"] = content.id
        mutable_data["object"] = object

        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)