from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models as m


class Account(User):
    # first/last name and email are inherited from User
    avatar = m.ImageField(upload_to='account_avatars/')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be in the format: '+999999999', with a maximum of 15 digits" )
    phone_number = m.CharField(validators=[phone_regex], max_length=250, null=True, blank=True)

class CurrentSubscription(m.Model):
    account = m.ForeignKey('Account', on_delete=m.CASCADE, related_name='current_subscription')
    plan = m.ForeignKey('subscriptions.SubscriptionPlan', on_delete=m.CASCADE, related_name='current_subscription')
    expiration = m.DateTimeField()

class EnrollClass(m.Model):
    account = m.ForeignKey('Account', on_delete=m.CASCADE, related_name='enroll_class')
    classtime = m.ForeignKey('classes.ClassTimeTable', on_delete=m.CASCADE, related_name='enroll_class')