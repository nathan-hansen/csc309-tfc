from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from classes.models import Class
from classes.serializers import ClassSerializer

from classes.utils import get_classes_with_spots, get_user_classes
# Create your views here.

class ClassView(generics.RetrieveAPIView):
    serializer_class = ClassSerializer

    def get_object(self):
        return get_object_or_404(Class, id=self.kwargs['class'])

class ListUpcomingClassView(generics.ListAPIView):
    serializer_class = ClassSerializer

    def get_queryset(self):
        return get_classes_with_spots()

class ListMyClassView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ClassSerializer

    def get_queryset(self):
        return get_user_classes(self.request.user)

class EnrollClassView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ClassSerializer

    def get_object(self):
        return get_object_or_404(Class, id=self.kwargs['class'])

    def perform_update(self, serializer):
        serializer.save()