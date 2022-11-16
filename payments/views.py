from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from payments.serializers import PaymentInfoSerializer, PaymentHistorySerializer
from payments.models import PaymentInfo, PaymentHistory
from django.utils import timezone
from django.shortcuts import get_object_or_404


# Create your views here.

class CreatePaymentInfoView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentInfo


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
        # first filter by payments of logged-in user, then filter for past payments
        user_queryset = PaymentHistory.objects.filter(account=self.request.user).filter(timestamp__gte=timezone.now())
        # then order by most recent and return
        return user_queryset.order_by('timestamp')
