from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from studios.serializers import StudioSerializer
from studios.models import Studio

# admin authenticated views
class CreateStudioView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = StudioSerializer


class UpdateStudioView(generics.UpdateAPIView):
    serializer_class = StudioSerializer
    queryset = Studio.objects.all()
    permission_classes = [IsAdminUser]
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

class DeleteStudioView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer

# user authenticated views
class ListStudioByProximityView(generics.ListAPIView):
    serializer_class = StudioSerializer
    queryset = Studio.objects.all()
    pass

class StudioView(generics.RetrieveAPIView):
    serializer_class = StudioSerializer

    def get_object(self):
        return get_object_or_404(Studio, id=self.kwargs['pk'])
