from django.db import models as m


class Studio(m.Model):
    name = m.CharField(max_length=250)
    address = m.CharField(max_length=250)
    latitude = m.FloatField()
    longitude = m.FloatField()
    postal_code = m.CharField(max_length=250)
    phone_number = m.CharField(max_length=250)


class StudioImage(m.Model):
    studio = m.ForeignKey('Studio', on_delete=m.CASCADE, related_name='image')
    image = m.ImageField()

class Amenities(m.Model):
    studio = m.ForeignKey('Studio', on_delete=m.CASCADE, related_name='amenities')
    type = m.CharField(max_length=250)
    quantity = m.IntegerField()