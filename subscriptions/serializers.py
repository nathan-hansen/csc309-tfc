from rest_framework.serializers import ModelSerializer, ValidationError
from subscriptions.models import SubscriptionPlan, CurrentSubscription
from payments.serializers import PaymentInfoSerializer
import datetime

class SubscriptionPlanSerializer(ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = [
                'price',
                'interval',
                ]


class CurrentSubscriptionSerializer(ModelSerializer):

    class Meta:
        model = CurrentSubscription
        fields = [
                'account',
                'studio',
                'plan',
                ]
    def validate(self, data):
        super().validate(data)
        if 'expiration' in data:
            raise ValidationError('cannot send expiration value')
        else:
            try:
                interval = SubscriptionPlan.objects.get(id=data['plan'].pk).interval
                today = datetime.datetime.combine(datetime.datetime.today(), 
                        datetime.datetime.min.time())
                if interval == 'yearly':
                    expiry = today.replace(year=today.year + 1, month=1, day=1)
                elif interval == 'monthly':
                    if today.month == 12:
                        expiry = today.replace(year=today.year + 1, month=1, day=1)
                    else:
                        expiry = today.replace(month=today.month + 1, day=1)

                elif interval == 'weekly':
                    pass

                elif interval == 'daily':
                    pass

                data['expiration'] = expiry

                return data


            except AttributeError:
                data['expiration'] = None
                return data

class CreateUserSubscriptionSerializer(ModelSerializer):

    payment_info = PaymentInfoSerializer
    fields = []
