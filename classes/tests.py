from django.test import TestCase
from django.utils import timezone

from django.contrib.auth.models import User
from django.test.client import Client
from studios.models import Studio
from classes.models import Class, ClassTimeTable, Keywords, EnrollClass

from accounts.models import Account

import random, datetime, json


# Create your tests here.
class TestClasses(TestCase):
    studio = None
    class_past = [] # list of tuples of (Class, Keywords)
    class_future = []
    class_enrolltest = Class

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
            coach='fake coach {}'.format(i),
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
            coach='fake coach {}'.format(i),
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
            coach='fake coach {}'.format(i),
            class_start=class_end - datetime.timedelta(days=random.randint(1, 100)),
            class_end=class_end,
            class_time=datetime.datetime.now().time(),
            duration=datetime.timedelta(minutes=random.randint(30, 120)),
            days_inbetween=random.randint(1, 7),
            spots=random.randint(1, 20),
        ) for i in range(random.randint(1, 10))]

        self.class_enrolltest = Class.objects.create(
            studio=self.studio,
            name='class enroll test',
            description='fake description',
            coach='fake coach {}'.format(1),
            class_start=datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 30)),
            class_end=datetime.datetime.now() + datetime.timedelta(days=random.randint(40, 60)),
            class_time=datetime.datetime.now().time(),
            duration=datetime.timedelta(minutes=random.randint(30, 120)),
            days_inbetween=random.randint(1, 7),
            spots=1,
        )


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

        # test if the response is sorted by time
        for i in range(len(response_list) - 1):
            self.assertTrue(response_list[i]['time'] <= response_list[i+1]['time'])
        
        # test filters
        response = client.get(f'/classes/{self.studio.id}/upcoming/?classid__coach=fake%20coach%201')
        self.assertEqual(response.status_code, 200)
        response_list = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(response_list), len(
            ClassTimeTable.objects.filter(time__gte=timezone.now()).\
            filter(spotleft__gt=0).\
            filter(classid__in=Class.objects.filter(studio=self.studio).\
            filter(coach='fake coach 1')))
        )


    def test_enroll(self):
        self.SetUp()

        client = Client()
        user1 = Account.objects.create_user(username='test1', password='test')
        client.login(username='test1', password='test')

        classtime_list = ClassTimeTable.objects.filter(classid=self.class_enrolltest)
        self.assertTrue(len(classtime_list) != 0)
        for i in classtime_list:
            response = client.post(f'/classes/modify/', {'timeid': i.id, 'op': 'enroll'})
            self.assertEqual(response.status_code, 200)
            response = json.loads(response.content.decode('utf-8'))
            self.assertTrue(response['message'] == 'Enrolled')

        # check if the spotleft is 0
        for i in classtime_list:
            self.assertTrue(ClassTimeTable.objects.get(id=i.id).spotleft == 0)

        # check if the user is enrolled
        for i in classtime_list:
            self.assertTrue(i in [j.classtime for j in EnrollClass.get_user_enroll(account=user1)])

        # enroll again as the same user
        for i in classtime_list:
            response = client.post(f'/classes/modify/', {'timeid': i.id, 'op': 'enroll'})
            self.assertEqual(response.status_code, 400)
            response = json.loads(response.content.decode('utf-8'))
            self.assertEqual(response['error'], 'Already enrolled')

        # enroll again as another user, should fail
        Account.objects.create_user(username='test2', password='test')
        client.login(username='test2', password='test')
        for i in classtime_list:
            response = client.post(f'/classes/modify/', {'timeid': i.id, 'op': 'enroll'})
            self.assertEqual(response.status_code, 400)
            response = json.loads(response.content.decode('utf-8'))
            self.assertEqual(response['error'], 'Class is full')


    def test_drop(self):
        self.SetUp()

        client = Client()
        user1 = Account.objects.create_user(username='test1', password='test')
        client.login(username='test1', password='test')

        classtime_list = ClassTimeTable.objects.filter(classid=self.class_enrolltest)
        self.assertTrue(len(classtime_list) != 0)
        for i in classtime_list:
            response = client.post(f'/classes/modify/', {'timeid': i.id, 'op': 'enroll'})
            self.assertEqual(response.status_code, 200)
            response = json.loads(response.content.decode('utf-8'))
            self.assertTrue(response['message'] == 'Enrolled')

        # check if the spotleft is 0
        for i in classtime_list:
            self.assertTrue(ClassTimeTable.objects.get(id=i.id).spotleft == 0)

        # drop the class
        for i in classtime_list:
            response = client.post(f'/classes/modify/', {'timeid': i.id, 'op': 'drop'})
            self.assertEqual(response.status_code, 200)
            response = json.loads(response.content.decode('utf-8'))
            self.assertTrue(response['message'] == 'Dropped')

        # check if the spotleft is 1
        for i in classtime_list:
            self.assertTrue(ClassTimeTable.objects.get(id=i.id).spotleft == 1)

        # check if the user is enrolled
        for i in classtime_list:
            self.assertTrue(i not in [j.classtime for j in EnrollClass.get_user_enroll(account=user1)])
        
        # drop again
        for i in classtime_list:
            response = client.post(f'/classes/modify/', {'timeid': i.id, 'op': 'drop'})
            self.assertEqual(response.status_code, 400)
            response = json.loads(response.content.decode('utf-8'))
            self.assertEqual(response['error'], 'Not enrolled')

        # drop again as another user, should fail
        Account.objects.create_user(username='test2', password='test')
        client.login(username='test2', password='test')
        for i in classtime_list:
            response = client.post(f'/classes/modify/', {'timeid': i.id, 'op': 'drop'})
            self.assertEqual(response.status_code, 400)
            response = json.loads(response.content.decode('utf-8'))
            self.assertEqual(response['error'], 'Not enrolled')

    def test_class_history(self):
        self.SetUp()

        client = Client()
        user1 = Account.objects.create_user(username='test1', password='test')
        client.login(username='test1', password='test')

        
        total_list = []
        # enroll past class
        for class_ in self.class_past:
            classtime_list = ClassTimeTable.objects.filter(classid=class_)
            total_list += classtime_list
            self.assertTrue(len(classtime_list) != 0)

            for i in classtime_list:
                response = client.post(f'/classes/modify/', {'timeid': i.id, 'op': 'enroll'})
                self.assertEqual(response.status_code, 200)
                response = json.loads(response.content.decode('utf-8'))
                self.assertTrue(response['message'] == 'Enrolled')

        # enroll future class
        for class_ in self.class_future:
            classtime_list = ClassTimeTable.objects.filter(classid=class_)
            total_list += classtime_list
            self.assertTrue(len(classtime_list) != 0)

            for i in classtime_list:
                response = client.post(f'/classes/modify/', {'timeid': i.id, 'op': 'enroll'})
                self.assertEqual(response.status_code, 200)
                response = json.loads(response.content.decode('utf-8'))
                self.assertTrue(response['message'] == 'Enrolled')

        # get history and schedule
        response = client.get(f'/classes/{self.studio.id}/schedule/')
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode('utf-8'))
        
        self.assertEqual(len(response["results"]), len(total_list))
