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
from rest_framework.response import Response


class SubscribeView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CurrentSubscriptionSerializer

    # add validation logic to create
    # based off this: https://stackoverflow.com/q/45981835
    def create(self, request, *args, **kwargs):
        # add code to check if an account with this subscription already exists
        current_account_id = self.request.user.id
        current_account = get_object_or_404(Account, pk=current_account_id)
        # it shouldn't ever 404 here because this is an authenticated view
        # maybe we should add a check here?

        # check if subscription with this account exists
        if CurrentSubscription.objects.filter(account=current_account).exists():
            return Response({'error': 'Subscription already exists for this user'}, status=400)
        # otherwise keep the existing create view api logic
        return super(SubscribeView, self).create(request, *args, **kwargs)


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
