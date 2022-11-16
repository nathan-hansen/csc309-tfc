from django.urls import path
from payments.views import (
        CreatePaymentInfoView,
        PaymentInfoUpdateView,
        ListPaymentHistory,
        ListPaymentUpcoming,
        )

app_name = 'payments'

urlpatterns = [
        path('add/', CreatePaymentInfoView.as_view()),
        path('update/', PaymentInfoUpdateView.as_view()),
        path('history/', ListPaymentHistory.as_view()),
        path('upcoming/', ListPaymentUpcoming.as_view()),
]

