from django.db import models as m


class PaymentInfo(m.Model):
    account = m.ForeignKey('accounts.Account', on_delete=m.CASCADE, related_name='payment_info')
    card_number = m.CharField(max_length=250)
    expiry_date = m.DateField()
    cvv = m.IntegerField()
    name_on_card = m.CharField(max_length=250)

class PaymentHistory(m.Model):
    account = m.ForeignKey('accounts.Account', on_delete=m.CASCADE, related_name='payment_history')
    timestamp = m.DateField()
    amount = m.FloatField()
    card_number = m.CharField(max_length=250)
    card_expiry = m.DateField()