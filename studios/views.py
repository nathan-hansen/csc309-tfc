from django.shortcuts import get_object_or_404
from geopy.distance import geodesic
from rest_framework import generics
from studios.serializers import (
        StudioSerializer, 
        StudioImageSerializer, 
        AmenitiesSerializer
        )
from studios.models import Studio, StudioImage, Amenities

# user authenticated views
class ListStudioByProximityView(generics.ListAPIView):
    serializer_class = StudioSerializer
    def get_queryset(self):
        lat = float(self.kwargs['latitude'])
        lon = float(self.kwargs['longitude'])
        print(f'lat: {lat}, lon: {lon}')
        return Studio.get_locations_nearby_coords(lat, lon)

class StudioView(generics.RetrieveAPIView):
    serializer_class = StudioSerializer

    def get_object(self):
        return get_object_or_404(Studio, id=self.kwargs['studio'])

# views for related models
class ListStudioImagesView(generics.ListAPIView):
    serializer_class = StudioImageSerializer
    def get_queryset(self):
        return StudioImage.objects.filter(studio=self.kwargs['studio'])

class ListAmenitiesView(generics.ListAPIView):
    serializer_class = AmenitiesSerializer
    def get_queryset(self):
        return Amenities.objects.filter(studio=self.kwargs['studio'])

