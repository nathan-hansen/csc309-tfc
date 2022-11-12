from django.db import models as m


class Class(m.Model):
    studio = m.ForeignKey('studios.Studio', on_delete=m.CASCADE, related_name='tfc_class')
    name = m.CharField(max_length=250)
    description = m.TextField()
    coach = m.CharField(max_length=250)
    keywords = m.TextField()
    capacity = m.IntegerField()
    start_time = m.DateTimeField()
    duration = m.DurationField()
