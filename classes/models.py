from django.db import models as m

class Class(m.Model):
    studio = m.ForeignKey('Studio', on_delete=m.SET_NULL, related_name='studio')
    name = m.CharField()
    description = m.TextField()
    coach = m.CharField()
    keywords = m.TextField()
    capacity = m.IntegerField()
    start_time = m.DateTimeField()
    duration = m.DurationField()
