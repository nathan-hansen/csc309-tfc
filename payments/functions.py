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
    Take in an account id and generate the serialized most recent Payment History
    of that account from the database, or return an error.
    """
    current_account = get_object_or_404(Account, id=account_id)
    # check if user has a subscription or payment info
    # check if payment info with this user exists, if not, raise error
    if not PaymentInfo.objects.filter(account=current_account).exists():
        return {'error': 'No upcoming payments, User has no payment info'}, None, None
    if not CurrentSubscription.objects.filter(account=current_account).exists():
        return {'error': 'No upcoming payments, User is not subscribed'}, None, None
    # get object or 404 should never trigger here, due to checks above
    current_subscription = get_object_or_404(CurrentSubscription, account=current_account)
    # check if current subscription is expired
    # current_subscription.expiration is timezone aware, so to compare it to datetime.now(), add timezone
    timezone_info = current_subscription.expiration.tzinfo
    if current_subscription.expiration < datetime.datetime.now(timezone_info):
        return {'error': 'No upcoming payments, subscription expired'}, None, None

    # if current subscription is null, return accordingly
    if current_subscription.plan is None:
        return {'error': 'You are not subscribed'}, None, None
    # id of the plan should be stored in plan attribute
    current_plan_id = current_subscription.plan.id
    sub_plan = get_object_or_404(SubscriptionPlan, id=current_plan_id)
    amount = sub_plan.payment

    # get the most recent past Payment and record payment info and time it was made
    history_queryset = PaymentHistory.objects.filter(account=current_account).filter(
        timestamp__lte=timezone.now())
    most_recent_payment = history_queryset.distinct().order_by('-timestamp')[0]
    # user payment credentials
    user_payment_info = PaymentInfo.objects.filter(account=current_account)[0]
    card_number = user_payment_info.card_number
    card_expiry = user_payment_info.expiry_date
    # set the time attribute of future payment
    most_recent_payment_time = most_recent_payment.timestamp
    # calculate the date of the upcoming payment
    interval = sub_plan.interval
    future_time = None
    if interval == "monthly":
        if most_recent_payment_time.month == 12:
            future_time = most_recent_payment_time.replace(year=most_recent_payment_time.year + 1, month=1)
        else:
            future_time = most_recent_payment_time.replace(month=most_recent_payment_time.month + 1)
    elif interval == "yearly":
        future_time = most_recent_payment_time.replace(year=most_recent_payment_time.year + 1)
    # create PaymentHistory object for upcoming payment
    upcoming_payment = PaymentHistory(account=current_account, timestamp=future_time, amount=amount,
                                      card_number=card_number, card_expiry=card_expiry)
    upcoming_payment_data = PaymentHistorySerializer(upcoming_payment).data
    return upcoming_payment_data, interval, current_subscription.expiration
