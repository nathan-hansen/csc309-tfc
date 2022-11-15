from django.urls import path
from studios.views import (
        ListStudioByProximityView,
        StudioView,
        ListStudioImagesView,
        ListAmenitiesView,
        )

app_name = 'studios'

urlpatterns = [
        path('list/<latitude>,<longitude>', ListStudioByProximityView.as_view()),
        path('<int:studio>/', StudioView.as_view()),
        path('<int:studio>/images/', ListStudioImagesView.as_view()),
        path('<int:studio>/amenities/', ListAmenitiesView.as_view()),
]

