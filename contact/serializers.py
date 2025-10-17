from rest_framework import serializers
from .models import ContactInfo, SocialLink, WalletInfo, BankDetail


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = '__all__'


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = '__all__'


class WalletInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletInfo
        fields = '__all__'


class BankDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetail
        fields = '__all__'