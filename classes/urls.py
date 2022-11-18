from django.urls import path

from classes.views import (
    ListUpcomingClassView,
    ListMyClassView,
    ModifyClassView,
)

app_name = 'classes'

urlpatterns = [
    path('<int:studio_id>/upcoming/', ListUpcomingClassView.as_view(), name='upcoming'),
    path('<int:studio_id>/schedule/', ListMyClassView.as_view(), name='schedule'),
    path('modify/', ModifyClassView.as_view(), name='modify'),
]

