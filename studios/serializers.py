from rest_framework.serializers import ModelSerializer
from studios.models import Studio

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
