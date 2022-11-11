from django.db import models as m

class Payment(m.Model):
    user = m.ForeignKey('accounts.User', on_delete=m.CASCADE, related_name='user_payment')
    card_number = m.IntegerField()
    card_expiry = m.IntegerField()
    card_security = m.IntegerField()
    current_subscription = m.ForeignKey('subscriptions.Subscription', null=True, on_delete=m.SET_NULL, related_name='current_subscription_payment')


class PaymentHistory(m.Model):
    user = m.ForeignKey('accounts.User', on_delete=m.CASCADE, related_name='payment_history')
    timestamp = m.DateTimeField()
    amount = m.DecimalField(decimal_places=2, max_digits=12)

