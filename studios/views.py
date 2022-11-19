from django.shortcuts import get_object_or_404
from geopy.distance import geodesic
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from studios.serializers import (
        StudioSerializer, 
        StudioImageSerializer, 
        AmenitiesSerializer
        )
from studios.models import Studio, StudioImage, Amenities

# user authenticated views
class ListStudioByProximityView(generics.ListAPIView):
    serializer_class = StudioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name', 'amenities__amenity_type', 'tfc_class__name', 'tfc_class__coach']
    search_fields = ['name', 'amenities__amenity_type', 'tfc_class__name', 'tfc_class__coach']
    def get_queryset(self):
        lat = float(self.kwargs['latitude'])
        lon = float(self.kwargs['longitude'])

        queryset = Studio.get_locations_nearby_coords(lat, lon)

        # search queries
        # studio_name = self.request.query_params.get('studio_name')
        # amenity = self.request.query_params.get('amenity')
        # class_name = self.request.query_params.get('class_name')
        # coach = self.request.query_params.get('coach')
        # if studio_name is not None:
        #     queryset = queryset.filter(name=studio_name)
        # if amenity is not None:
        #     # get amenity if exists
        #     amenity_queryset = Amenities.objects.filter(amenity_type=amenity)




        return queryset

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

