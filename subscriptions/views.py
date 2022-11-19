from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from subscriptions.models import CurrentSubscription, SubscriptionPlan
from subscriptions.serializers import (
    SubscriptionPlanSerializer,
    CurrentSubscriptionSerializer,
)
from django.shortcuts import get_object_or_404
from payments.models import PaymentInfo, PaymentHistory
from accounts.models import Account
from rest_framework.response import Response
import datetime
from payments.functions import create_payment_history


class SubscribeView(generics.CreateAPIView):
    """
    Allows a user to subscribe. Prerequisites:
    - This account does not have a subscription 
    (or a previously cancelled subscription - in which case the UpdateView should instead be used.)
    - This account has registered payment information
    
    This method creates:
    - a CurrentSubscription entry for this user
    - an entry in PaymentHistory logging this transaction
    """
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
        # check if payment info with this user exists, if not, raise error
        if not PaymentInfo.objects.filter(account=current_account).exists():
            return Response({'error': 'User does not have Payment Info to subscribe'}, status=400)
        # otherwise keep the existing create view api logic
        created_subscription = super(SubscribeView, self).create(request, *args, **kwargs)
        new_current_sub_plan_id = created_subscription.data.get('plan')

        # Create Payment History
        create_payment_history(current_account, new_current_sub_plan_id)
        return created_subscription


class UpdateSubscriptionView(generics.UpdateAPIView):
    """
    Allows a user to change their subscription plan to either a) another existing plan, or b) null (a cancellation).
    If a user changes to a non-null subscription plan, the newer expiry date is added to the old one,
    and a new payment is created to reflect coverage to next expiry date.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CurrentSubscriptionSerializer

    def get_object(self, **kwargs):
        # return CurrentSubscription.objects.filter(account=self.kwargs['pk'], id=self.kwargs['subscription'])
        current_account = get_object_or_404(Account, id=self.request.user.id)
        # use get object or 404 because we are updating specific current subscription with an id and account
        # use current_account because we only want logged-in user to be able to edit their subscriptions
        current_sub = get_object_or_404(CurrentSubscription, account=current_account)
        sub_plan_id = self.request.data['plan']
        if sub_plan_id != "":  # if the user did not unsubscribe, but picked yearly or monthly
            create_payment_history(current_account, sub_plan_id)
        return current_sub
        # will return "Not found" if current subscription does not belong to user
