from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from subscriptions.models import CurrentSubscription
from subscriptions.serializers import (
        SubscriptionPlanSerializer,
        CurrentSubscriptionSerializer,
        )


class SubscribeView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CurrentSubscriptionSerializer

class UpdateSubscriptionView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CurrentSubscriptionSerializer
    def get_queryset(self):
        return CurrentSubscription.objects.filter(account=self.kwargs['pk'], id=self.kwargs['subscription'])

class CancelSubscriptionView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CurrentSubscriptionSerializer
    def get_queryset(self):
        return CurrentSubscription.objects.filter(account=self.kwargs['pk'], id=self.kwargs['subscription'])

