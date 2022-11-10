from django.db import models as m
from django.contrib.auth.models import User

class User(User):
    avatar = ImageField()
    phone_number = IntegerField()
