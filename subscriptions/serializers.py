from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.validators import UniqueValidator
from subscriptions.models import SubscriptionPlan, CurrentSubscription
from payments.serializers import PaymentInfoSerializer
from accounts.serializers import AccountSerializer
from accounts.models import Account
from django.shortcuts import get_object_or_404
import datetime


class SubscriptionPlanSerializer(ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = [
            'price',
            'interval',
        ]


class CurrentSubscriptionSerializer(ModelSerializer):
    account = AccountSerializer

    class Meta:
        model = CurrentSubscription
        fields = [
            'account',
            'plan',
            'expiration',
        ]
        read_only_fields = ['account', 'expiration']

    def validate(self, data):
        super().validate(data)
        if 'expiration' in data:
            raise ValidationError('cannot send expiration value')
        # validate the interval in plan if there is a plan submitted
        if data.get('plan') is not None:
            interval = SubscriptionPlan.objects.get(id=data['plan'].pk).interval
            if interval not in ("monthly", "yearly"):
                raise ValidationError('invalid interval')
        return data
        # else:
        #     try:
        #         interval = SubscriptionPlan.objects.get(id=data['plan'].pk).interval
        #         today = datetime.date.today()
        #         if interval == 'yearly':
        #             expiry = today.replace(year=today.year + 1, month=1, day=1)
        #         elif interval == 'monthly':
        #             if today.month == 12:
        #                 expiry = today.replace(year=today.year + 1, month=1, day=1)
        #             else:
        #                 expiry = today.replace(month=today.month + 1, day=1)
        #
        #         elif interval == 'weekly':
        #             pass
        #
        #         elif interval == 'daily':
        #             pass
        #
        #         data['expiration'] = expiry
        #
        #         return data
        #
        #
        #     except AttributeError:
        #         return data

    # reference to override create method to pre-set attribute to logged-in user:
    # https://stackoverflow.com/a/58430009
    def create(self, validated_data):
        current_account_id = self.context['request'].user.id
        current_account = get_object_or_404(Account, pk=current_account_id)
        interval = SubscriptionPlan.objects.get(id=validated_data['plan'].pk).interval
        today = datetime.date.today()
        if interval == 'yearly':
            expiry = today.replace(year=today.year + 1)
        elif interval == 'monthly':
            if today.month == 12:
                expiry = today.replace(year=today.year + 1, month=1, day=1)
            else:
                expiry = today.replace(month=today.month + 1)
        else:
            raise ValidationError('invalid interval')
        return CurrentSubscription.objects.create(account=current_account, 
                                                  plan=validated_data['plan'], expiration=expiry)
