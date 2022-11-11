from django.db import models as m

class Subscription(m.Model):
    payment = m.DecimalField(decimal_places=2, max_digits=12)
    # TODO: interval should be one of 'weekly', 'yearly', 'daily', etc
    interval = m.CharField(max_length=16)
