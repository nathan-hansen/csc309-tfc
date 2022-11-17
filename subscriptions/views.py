from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from subscriptions.models import CurrentSubscription
from subscriptions.serializers import (
    SubscriptionPlanSerializer,
    CurrentSubscriptionSerializer,
)
from django.shortcuts import get_object_or_404
from accounts.models import Account


class SubscribeView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CurrentSubscriptionSerializer


class UpdateSubscriptionView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CurrentSubscriptionSerializer

    def get_object(self, **kwargs):
        # return CurrentSubscription.objects.filter(account=self.kwargs['pk'], id=self.kwargs['subscription'])
        current_account = get_object_or_404(Account, id=self.request.user.id)
        # use get object or 404 because we are updating specific current subscription with an id and account
        # use current_account because we only want logged-in user to be able to edit their subscriptions
        return get_object_or_404(CurrentSubscription, account=current_account)
        # will return "Not found" if current subscription does not belong to user


class CancelSubscriptionView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CurrentSubscriptionSerializer

    # def get_queryset(self):
    #     return CurrentSubscription.objects.filter(account=self.kwargs['pk'], id=self.kwargs['subscription'])
    def get_object(self, **kwargs):
        current_account = get_object_or_404(Account, id=self.request.user.id)
        # use get object or 404 because we are updating specific current subscription with an id and account
        # use current_account because we only want logged in user to be able to edit their subscriptions
        return get_object_or_404(CurrentSubscription, account=current_account)
        # will return "Not found" if current subscription does not belong to user
