from django.db import models as m

class Studio(m.Model):
    name = m.CharField(max_length=250)
    address = m.CharField(max_length=250)
    latitude = m.FloatField()
    longitude = m.FloatField()
    postal_code = m.CharField(max_length=250)
    phone_number = m.IntegerField()


class StudioImage(m.Model):
    studio = m.ForeignKey('Studio', on_delete=m.CASCADE, related_name='image')
    image = m.ImageField()
