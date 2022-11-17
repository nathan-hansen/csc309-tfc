from django.db import models as m


class SubscriptionPlan(m.Model):
    payment = m.DecimalField(decimal_places=2, max_digits=12)
    interval = m.CharField(max_length=16)

class CurrentSubscription(m.Model):
    account = m.ForeignKey('accounts.Account', on_delete=m.CASCADE, related_name='account_subscription')
    studio = m.ForeignKey('studios.Studio', on_delete=m.CASCADE, related_name='studio_subscription')
    plan = m.ForeignKey('SubscriptionPlan', on_delete=m.CASCADE, null=True, blank=True, related_name='current_plan')
    expiration = m.DateTimeField(null=True, blank=True)

