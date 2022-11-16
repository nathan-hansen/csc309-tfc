from rest_framework import serializers
from payments.models import PaymentInfo, PaymentHistory
from accounts.serializers import AccountSerializer


class PaymentInfoSerializer(serializers.ModelSerializer):
    account = AccountSerializer

    class Meta:
        model = PaymentInfo
        fields = ['account', 'name_on_card', 'card_number', 'cvv', 'expiry_date']


class PaymentHistorySerializer(serializers.ModelSerializer):
    account = AccountSerializer

    class Meta:
        model = PaymentHistory
        fields = ['account', 'timestamp', 'card_number', 'card_expiry']
