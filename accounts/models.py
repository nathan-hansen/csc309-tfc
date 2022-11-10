from django.db import models as m
from django.contrib.auth.models import User

class User(User):
    avatar = m.ImageField()
    phone_number = m.IntegerField()
