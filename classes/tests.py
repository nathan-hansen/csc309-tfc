from django.test import TestCase
from django.utils import timezone

from django.contrib.auth.models import User
from django.test.client import Client
from studios.models import Studio
from classes.models import Class, ClassTimeTable, Keywords

import random, datetime, json


# Create your tests here.
class TestClasses(TestCase):
    studio = None
    class_past = [] # list of tuples of (Class, Keywords)
    class_future = []

    def SetUp(self):
        self.studio = Studio.objects.create(
            name='fake studio',
            address='fake address',
            latitude=43.6532,
            longitude=-79.3832,
            postal_code='M5V 2T6',
            phone_number='1234567890',
        )

        class_start = datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 50))
        self.class_future = [Class.objects.create(
            studio=self.studio,
            name='fake class future {}'.format(i),
            description='fake description',
            coach='fake coach',
            class_start=class_start,
            class_end=class_start + datetime.timedelta(days=random.randint(1, 60)),
            class_time=datetime.datetime.now().time(),
            duration=datetime.timedelta(minutes=random.randint(30, 120)),
            days_inbetween=random.randint(1, 7),
            spots=random.randint(1, 20),
        ) for i in range(random.randint(1, 10))]  + \
        [Class.objects.create(
            studio=self.studio,
            name='fake class middle {}'.format(i),
            description='fake description',
            coach='fake coach',
            class_start=datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 50)),
            class_end=datetime.datetime.now() + datetime.timedelta(days=random.randint(7, 50)),
            class_time=datetime.datetime.now().time(),
            duration=datetime.timedelta(minutes=random.randint(30, 120)),
            days_inbetween=random.randint(1, 7),
            spots=random.randint(1, 20),
        ) for i in range(random.randint(1, 10))]

        class_end = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30))
        self.class_past = [Class.objects.create(
            studio=self.studio,
            name='fake class past {}'.format(i),
            description='fake description',
            coach='fake coach',
            class_start=class_end - datetime.timedelta(days=random.randint(1, 100)),
            class_end=class_end,
            class_time=datetime.datetime.now().time(),
            duration=datetime.timedelta(minutes=random.randint(30, 120)),
            days_inbetween=random.randint(1, 7),
            spots=random.randint(1, 20),
        ) for i in range(random.randint(1, 10))]


    def test_classes_upcoming(self):
        self.SetUp()

        client = Client()
        response = client.get(f'/classes/{self.studio.id}/upcoming/')
        self.assertEqual(response.status_code, 200)
        response_list = json.loads(response.content.decode('utf-8'))

        for i in response_list:
            self.assertTrue(i['time'] > datetime.datetime.now().strftime('%Y-%m-%d'))
        
        self.assertTrue(len(response_list) == len(
            ClassTimeTable.objects.filter(time__gte=timezone.now()).\
            filter(spotleft__gt=0).\
            filter(classid__in=Class.objects.filter(studio=self.studio)))
        )

    def test_enroll(self):
        self.SetUp()

        client = Client()
        user = User.objects.create_user(username='test', password='test')
        client.login(username='test', password='test')

        # for i in self.class_future:




            
