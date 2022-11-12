from django.contrib.auth.models import User
from django.db import models as m


class Account(User):
    # first/last name and email are inherited from User
    avatar = m.ImageField()
    phone_number = m.CharField(max_length=250)
    current_subscription = m.ForeignKey('subscriptions.CurrentSubscription', on_delete=m.SET_NULL, related_name='account')

class CurrentSubscription(m.Model):
    account = m.ForeignKey('Account', on_delete=m.CASCADE, related_name='current_subscription')
    plan = m.ForeignKey('subscriptions.SubscriptionPlan', on_delete=m.CASCADE, related_name='current_subscription')
    expiration = m.DateTimeField()

class EnrollClass(m.Model):
    account = m.ForeignKey('Account', on_delete=m.CASCADE, related_name='enroll_class')
    classtime = m.ForeignKey('classes.ClassTimeTable', on_delete=m.CASCADE, related_name='enroll_class')