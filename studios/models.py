from django.db import models as m
from django.contrib.gis.db import models as gm

class Studio(m.Model):
    name = m.CharField()
    address = m.CharField()
    location = gm.PointField()
    postal_code = m.CharField()
    phone_number = m.IntegerField()


class StudioImage(m.Model):
    studio = m.ForeignKey(Studio, on_delete=m.SET_NULL, related_name='studio')
    image = m.ImageField()
