from django.urls import path
from studios.views import (
        CreateStudioView,
        UpdateStudioView,
        DeleteStudioView,
        ListStudioByProximityView,
        StudioView,
        )

app_name = 'studios'

urlpatterns = [
        path('create/', CreateStudioView.as_view()),
        path('<int:pk>/update/', UpdateStudioView.as_view()),
        path('<int:pk>/delete/', DeleteStudioView.as_view()),
        path('list/', ListStudioByProximityView.as_view()),
        path('<int:pk>/', StudioView.as_view()),
]

