from rest_framework import serializers
from .models import Purpose, Sadaqah
from contact.models import WalletInfo, BankDetail


class PurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purpose
        fields = '__all__'


class SadaqahSerializer(serializers.ModelSerializer):
    purpose_name_bn = serializers.SerializerMethodField()
    payment_method = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Sadaqah
        fields = '__all__'

    def get_purpose_name_bn(self, obj):
        return obj.purpose.name_bn

    def get_payment_method(self, obj):
        if isinstance(obj.method, WalletInfo):
            return f"{obj.method.name} ({obj.method.number})"
        elif isinstance(obj.method, BankDetail):
            return f"{obj.method.name} ({obj.method.account})"
        return "Unknown"