from subscriptions.models import SubscriptionPlan, CurrentSubscription
from accounts.models import Account
from django.utils import timezone
from django.shortcuts import get_object_or_404
from payments.models import PaymentInfo, PaymentHistory
from payments.serializers import PaymentHistorySerializer
from rest_framework.response import Response
import datetime


def generate_upcoming_payment(account_id: int):
    """
    Take in an account id and return Upcoming payment based on the subscription plan
    and payment of that account from the database (returned as serialized Payment History),
    and return the recurrence interval, or return an error.
    """
    current_account = get_object_or_404(Account, id=account_id)
    # check if user has a subscription or payment info
    # check if payment info with this user exists, if not, raise error
    if not PaymentInfo.objects.filter(account=current_account).exists():
        return {'error': 'No upcoming payments, User has no payment info'}, None
    if not CurrentSubscription.objects.filter(account=current_account).exists():
        return {'error': 'No upcoming payments, User is not subscribed'}, None
    # get object or 404 should never trigger here, due to checks above
    current_subscription = get_object_or_404(CurrentSubscription, account=current_account)
    # if current subscription is null, return accordingly
    if current_subscription.plan is None:
        return {'error': 'You are not subscribed'}, None
    # check if current subscription is expired
    if current_subscription.expiration < datetime.date.today():
        return {'error': 'No upcoming payments, subscription expired'}, None

    # id of the plan should be stored in plan attribute
    current_plan_id = current_subscription.plan.id
    sub_plan = get_object_or_404(SubscriptionPlan, id=current_plan_id)
    # get the amount paid based on current subscription plan
    amount = sub_plan.payment
    # Find the recurrence of the current subscription plan
    interval = sub_plan.interval

    # user payment credentials from current payment method
    user_payment_info = PaymentInfo.objects.filter(account=current_account)[0]
    card_number = user_payment_info.card_number
    card_expiry = user_payment_info.expiry_date
    # the future time of the payment is based on when the current subscription expires
    future_time = current_subscription.expiration
    upcoming_payment = PaymentHistory(account=current_account, timestamp=future_time, amount=amount,
                                      card_number=card_number, card_expiry=card_expiry)
    upcoming_payment_data = PaymentHistorySerializer(upcoming_payment).data
    return upcoming_payment_data, interval


def create_payment_history(current_account: Account, sub_plan_id: int):
    """
    Create a Payment History with timestamp of today for Account current_account
    based on the subscription plan with id sub_plan_id
    """
    current_payment_info = get_object_or_404(PaymentInfo, account=current_account)
    card_number = current_payment_info.card_number
    card_expiry = current_payment_info.expiry_date
    sub_plan = get_object_or_404(SubscriptionPlan, id=sub_plan_id)
    amount = sub_plan.payment
    today = datetime.date.today()
    PaymentHistory.objects.create(account=current_account, timestamp=today, amount=amount, card_number=card_number,
                                  card_expiry=card_expiry)
    return

