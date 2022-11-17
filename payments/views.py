from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from payments.serializers import PaymentInfoSerializer, PaymentHistorySerializer
from payments.models import PaymentInfo, PaymentHistory
from accounts.models import Account
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


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
        return user_queryset.order_by('timestamp')


class ListPaymentUpcoming(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentHistorySerializer

    def get_queryset(self):
        # first filter by payments of logged-in user, then filter for future payments
        user_queryset = PaymentHistory.objects.filter(account=self.request.user).filter(timestamp__gte=timezone.now())
        # then order by most recent and return
        return user_queryset.order_by('timestamp')
