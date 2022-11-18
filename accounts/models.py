from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models as m


class Account(User):
    # first/last name and email are inherited from User
    avatar = m.ImageField(upload_to='account_avatars/', null=True, blank=True)
    # phone number regex from: https://stackoverflow.com/a/19131360
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be in the format: '+999999999', with a maximum of 15 digits" )
    phone_number = m.CharField(validators=[phone_regex], max_length=250, null=True, blank=True)

