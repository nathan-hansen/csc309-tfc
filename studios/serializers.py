from rest_framework.serializers import ModelSerializer, SlugRelatedField
from studios.models import Studio, StudioImage, Amenities

class StudioSerializer(ModelSerializer):
    class Meta:
        model = Studio
        fields = [
                'name',
                'address',
                'latitude',
                'longitude',
                'postal_code',
                'phone_number',
                ]


class StudioImageSerializer(ModelSerializer):
    studio = SlugRelatedField(
            queryset = Studio.objects.all(), slug_field = 'pk'
            )
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(StudioImageSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = StudioImage
        fields = [
                'studio',
                'image',
                ]


class AmenitiesSerializer(ModelSerializer):
    class Meta:
        model = Amenities
        fields = [
                'studio',
                'amenity_type',
                'quantity',
                ]
