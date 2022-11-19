import datetime

from django.db import models as m
from rest_framework.validators import UniqueValidator


class SubscriptionPlan(m.Model):
    payment = m.DecimalField(decimal_places=2, max_digits=12)
    interval = m.CharField(max_length=16)


class CurrentSubscription(m.Model):
    account = m.OneToOneField('accounts.Account', on_delete=m.CASCADE, related_name='account_subscription')
    plan = m.ForeignKey('SubscriptionPlan', on_delete=m.CASCADE, null=True, blank=True, related_name='current_plan')
    expiration = m.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # use this to override update and change expiry date based on the old value
        if self.pk:
            current_sub = CurrentSubscription.objects.get(id=self.pk)
            current_expiry = current_sub.expiration
            # if we update and the previous value is Null but new value for plan is not null
            # set expiration date to today, as if you were creating it
            if current_expiry is None:
                current_expiry = datetime.date.today()
            # if the new updated value is for plan is not None, calculate expiry date
            if self.plan is not None:
                plan_interval = self.plan.interval
                if plan_interval == "monthly":
                    if current_expiry.month == 12:
                        self.expiration = current_expiry.replace(year=current_expiry.year + 1, month=1)
                    else:
                        self.expiration = current_expiry.replace(month=current_expiry.month + 1)
                elif plan_interval == "yearly":
                    self.expiration = current_expiry.replace(year=current_expiry.year + 1)
            else:
                self.expiration = None
        super(CurrentSubscription, self).save(*args, **kwargs)
