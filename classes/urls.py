from django.urls import path

from classes.views import (
    ListUpcomingClassView,
    ListMyClassView,
    ModifyClassView,
)

app_name = 'classes'

urlpatterns = [
    path('<int:studio_id>/upcoming/', ListUpcomingClassView.as_view(), name='upcoming'),
    path('history/', ListMyClassView.as_view(), name='history'),
    path('modify/', ModifyClassView.as_view(), name='modify'),
]

