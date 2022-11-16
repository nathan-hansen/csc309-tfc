from rest_framework import serializers

from classes.models import Class, ClassTimeTable, Keywords


class KeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keywords
        fields = ('id', 'keyword')


class ClassTimeTableSerializer(serializers.ModelSerializer):
    ''' As a user, I want to see the class schedule of a specific studio on its page. 
    Classes must appear in the order of their start time (from now), and the class information must be shown. 
    Past or cancelled classes should not be listed.'''
    class Meta:
        model = ClassTimeTable
        fields = ['time', 'spotleft']


class ClassSerializer(serializers.ModelSerializer):
    '''As the website admin, I can create/edit a class in a specific studio. 
    A class has a name, description, coach, a list of keywords (e.g., upper-body, core, etc.), 
    capacity, and times. '''
    keywords = KeywordsSerializer(many=True, read_only=True)
    timetable = ClassTimeTableSerializer(many=True, read_only=True)

    class Meta:
        model = Class
        fields = ['name', 'description', 'coach', 'keywords', 'timetable']
