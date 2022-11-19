from rest_framework import serializers
from payments.models import PaymentInfo, PaymentHistory
from accounts.serializers import AccountSerializer
from django.shortcuts import get_object_or_404
from accounts.models import Account


class PaymentInfoSerializer(serializers.ModelSerializer):
    account = AccountSerializer

    class Meta:
        model = PaymentInfo
        fields = ['account', 'name_on_card', 'card_number', 'cvv', 'expiry_date']
        read_only_fields = ['account']

    # override create method to pre-set the account attribute
    def create(self, validated_data):
        current_account_id = self.context['request'].user.id
        current_account = get_object_or_404(Account, pk=current_account_id)
        return PaymentInfo.objects.create(account=current_account, name_on_card=validated_data['name_on_card'],
                                          card_number=validated_data['card_number'], cvv=validated_data['cvv'],
                                          expiry_date=validated_data['expiry_date'])


class PaymentHistorySerializer(serializers.ModelSerializer):
    account = AccountSerializer

    class Meta:
        model = PaymentHistory
        fields = ['account', 'timestamp', 'amount', 'card_number', 'card_expiry']
