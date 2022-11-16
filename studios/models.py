from django.db import models as m
from django.db.models.expressions import RawSQL
from django.db.backends.signals import connection_created
from django.dispatch import receiver
import math


# Following method sourced from user @rphlo at
# https://stackoverflow.com/questions/19703975/django-sort-by-distance
@receiver(connection_created)
def extend_sqlite(connection=None, **kwargs):
    if connection.vendor == "sqlite":
        # sqlite doesn't natively support math functions, so add them
        cf = connection.connection.create_function
        cf('acos', 1, math.acos)
        cf('cos', 1, math.cos)
        cf('radians', 1, math.radians)
        cf('sin', 1, math.sin)
        cf('least', 2, min)
        cf('greatest', 2, max)


class Studio(m.Model):
    name = m.CharField(max_length=250)
    address = m.CharField(max_length=250)
    latitude = m.FloatField()
    longitude = m.FloatField()
    postal_code = m.CharField(max_length=250)
    phone_number = m.CharField(max_length=250)

    # Following method sourced from user @rphlo at
    # https://stackoverflow.com/questions/19703975/django-sort-by-distance
    def get_locations_nearby_coords(latitude, longitude, max_distance=None):
        """
        Return objects sorted by distance to specified coordinates
        which distance is less than max_distance given in kilometers
        """
        # Great circle distance formula
        gcd_formula = "6371 * acos(least(greatest(\
        cos(radians(%s)) * cos(radians(latitude)) \
        * cos(radians(longitude) - radians(%s)) + \
        sin(radians(%s)) * sin(radians(latitude)) \
        , -1), 1))"
        distance_raw_sql = RawSQL(
            gcd_formula,
            (latitude, longitude, latitude)
        )
        qs = Studio.objects.all() \
        .annotate(distance=distance_raw_sql) \
        .order_by('distance')
        if max_distance is not None:
            qs = qs.filter(distance__lt=max_distance)
        return qs

class StudioImage(m.Model):
    studio = m.ForeignKey('Studio', on_delete=m.CASCADE, related_name='image')
    image = m.ImageField(upload_to="studios/")


class Amenities(m.Model):
    studio = m.ForeignKey('Studio', on_delete=m.CASCADE, related_name='amenities')
    amenity_type = m.CharField(max_length=250)
    quantity = m.IntegerField()
    class Meta:
        verbose_name_plural = "Amenities"


