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
from payments.functions import generate_upcoming_payment
import datetime


class CreatePaymentInfoView(CreateAPIView):
    """
    Allows a user to register their credit card details.
    """
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
    """
    Allows a user to alter their credit card details.
    """
    permission_classes = [IsAuthenticated]
    # make sure user is logged in
    serializer_class = PaymentInfoSerializer

    def get_object(self):
        return get_object_or_404(PaymentInfo, account=self.request.user)


class ListPaymentHistory(ListAPIView):
    """
    Allows a user to view all their past payments on file, sorted by recent.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentHistorySerializer

    def get_queryset(self):
        # first filter by payments of logged-in user, then filter for past payments
        user_queryset = PaymentHistory.objects.filter(account=self.request.user).filter(timestamp__lte=timezone.now())
        # then order by most recent and return
        return user_queryset.order_by('-timestamp')


class PaymentUpcomingView(APIView):
    """
    Allows a user to view their next upcoming payment, and the payment recurrence interval.
    The next upcoming payment is when the coverage they have already paid for expires
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payment_history_data, interval = generate_upcoming_payment(self.request.user.id)
        if payment_history_data.get('error') is not None:
            return Response(payment_history_data, status=400)
        # else create the return data
        return_data = {"account": payment_history_data.get('account'),
                       "timestamp": payment_history_data.get('timestamp'), "amount": payment_history_data.get('amount'),
                       "card_number": payment_history_data.get('card_number'),
                       "card_expiry": payment_history_data.get('card_expiry'), "recurrence": interval}
        return Response(return_data, status=200)
