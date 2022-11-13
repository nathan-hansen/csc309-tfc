from django.db import models as m


class SubscriptionPlan(m.Model):
    payment = m.DecimalField(decimal_places=2, max_digits=12)
    interval = m.DurationField()

