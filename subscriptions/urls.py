from django.urls import path
from subscriptions.views import (
        SubscribeView,
        UpdateSubscriptionView,
        CancelSubscriptionView,
        )

app_name = 'subscriptions'

urlpatterns = [
        path('subscribe/', SubscribeView.as_view()),
        path('<int:pk>/update/<int:subscription>/', UpdateSubscriptionView.as_view()),
        path('<int:pk>/cancel/<int:subscription>/', CancelSubscriptionView.as_view()),
]

