from django.test import TestCase, Client
from django.contrib.auth.models import User
import random
from geopy.distance import great_circle
from studios.models import Studio, StudioImage, Amenities


# Create your tests here.
class StudioTest(TestCase):
    studios = []

    def create_user(self):
        self.username = "test_admin"
        self.password = User.objects.make_random_password()
        user, created = User.objects.get_or_create(username=self.username)
        user.set_password(self.password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        self.user = user

    def setUp(self) -> None:
        self.create_user()
        self.studios = [
            Studio.objects.create(
                name="studio{}".format(i),
                address="address{}".format(i),
                latitude=random.uniform(-90, 90),
                longitude=random.uniform(-180, 180),
                postal_code="postal_code{}".format(i),
                phone_number="1234567890",
            )
            for i in range(1, random.randint(1, 21))
        ]

    def test_list_studio_by_proximity(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        
            
        for i in range(20):
            cood = (random.uniform(-90, 90), random.uniform(-180, 180))
            response = c.get(
                "/studios/list/{},{}".format(cood[0], cood[1])
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['count'], len(self.studios))

            distance_list = [
                (great_circle(
                    (studio.latitude, studio.longitude), cood
                    ), studio)
                for studio in self.studios
            ]
            distance_list.sort(key=lambda x: x[0])

            for i in range(len(self.studios)):
                self.assertEqual(response.data["results"][i]["name"], distance_list[i][1].name)
        

