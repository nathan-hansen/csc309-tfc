from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from payments.serializers import PaymentInfoSerializer, PaymentHistorySerializer
from payments.models import PaymentInfo, PaymentHistory
from subscriptions.models import SubscriptionPlan, CurrentSubscription
from accounts.models import Account
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
import datetime


class CreatePaymentInfoView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentInfoSerializer

    # add validation logic to create
    # based off this: https://stackoverflow.com/q/45981835
    def create(self, request, *args, **kwargs):
        # add code to check if an account with this subscription already exists
        current_account_id = self.request.user.id
        current_account = get_object_or_404(Account, pk=current_account_id)
        # it shouldn't ever 404 here because this is an authenticated view
        # maybe we should add a check here?

        # check if subscription with this account exists
        if PaymentInfo.objects.filter(account=current_account).exists():
            return Response({'error': 'Payment Info already exists for this user'}, status=400)
        # otherwise keep the existing create view api logic
        return super(CreatePaymentInfoView, self).create(request, *args, **kwargs)


class PaymentInfoUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    # make sure user is logged in
    serializer_class = PaymentInfoSerializer

    def get_object(self):
        return get_object_or_404(PaymentInfo, account=self.request.user)


class ListPaymentHistory(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentHistorySerializer

    def get_queryset(self):
        # first filter by payments of logged-in user, then filter for past payments
        user_queryset = PaymentHistory.objects.filter(account=self.request.user).filter(timestamp__lte=timezone.now())
        # then order by most recent and return
        return user_queryset.order_by('-timestamp')


class PaymentUpcomingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_account = get_object_or_404(Account, id=self.request.user.id)
        # check if user has a subscription or payment info
        # check if payment info with this user exists, if not, raise error
        if not PaymentInfo.objects.filter(account=current_account).exists():
            return Response({'error': 'No upcoming payments, User has no payment info'}, status=400)
        if not CurrentSubscription.objects.filter(account=current_account).exists():
            return Response({'error': 'No upcoming payments, User is not subscribed'}, status=400)
        # get object or 404 should never trigger here, due to checks above
        current_subscription = get_object_or_404(CurrentSubscription, account=current_account)
        # check if current subscription is expired
        # current_subscription.expiration is timezone aware, so to compare it to datetime.now(), add timezone
        timezone_info = current_subscription.expiration.tzinfo
        if current_subscription.expiration < datetime.datetime.now(timezone_info):
            return Response({'error': 'No upcoming payments, subscription expired'}, status=400)

        # id of the plan should be stored in plan attribute
        current_plan_id = current_subscription.plan.id
        sub_plan = get_object_or_404(SubscriptionPlan, id=current_plan_id)
        amount = sub_plan.payment

        # get the most recent past Payment and record payment info and time it was made
        history_queryset = PaymentHistory.objects.filter(account=self.request.user).filter(
            timestamp__lte=timezone.now())
        most_recent_payment = history_queryset.distinct().order_by('-timestamp')[0]
        card_number = most_recent_payment.card_number
        card_expiry = most_recent_payment.card_expiry
        # set the time attribute of future payment
        most_recent_payment_time = most_recent_payment.timestamp
        # calculate the date of the upcoming payment
        interval = sub_plan.interval
        future_time = None
        if interval == "monthly":
            future_time = most_recent_payment_time.replace(month=most_recent_payment_time.month + 1)
        elif interval == "yearly":
            future_time = most_recent_payment_time.replace(year=most_recent_payment_time.year + 1)
        # create PaymentHistory object for upcoming payment
        upcoming_payment = PaymentHistory(account=current_account, timestamp=future_time, amount=amount,
                                          card_number=card_number, card_expiry=card_expiry)

        upcoming_payment_data = PaymentHistorySerializer(upcoming_payment).data
        return Response(upcoming_payment_data, status=200)
