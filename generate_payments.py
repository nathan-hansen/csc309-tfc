import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TFC.settings")
django.setup()
from payments.functions import generate_upcoming_payment
from payments.serializers import PaymentHistorySerializer
from accounts.models import Account
import datetime


def main():
    generate_payments_today()


def generate_payments_today():
    user_queryset = Account.objects.all()
    for user in user_queryset:
        # input the primary key or id of the account
        response_data = generate_upcoming_payment(user.pk)[0]
        if response_data.get('account') is not None:
            # should have returned PaymentHistory
            pay_time_str = response_data.get('timestamp')
            # convert datetime string in serialized object to datetime object
            # source: https://stackoverflow.com/a/13182163
            pay_time = datetime.date.fromisoformat(pay_time_str)
            # test_time = pay_time.replace(month=pay_time.month - 1)
            # in order to compare if payment is due today
            if pay_time == datetime.date.today():  # check if payment time is today
                # deserialize response data and save the PaymentHistory object
                payment_history = PaymentHistorySerializer(data=response_data)
                # check if deserialized is valid
                if payment_history.is_valid():
                    payment_history.save()


if __name__ == '__main__':
    main()
