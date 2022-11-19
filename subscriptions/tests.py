from django.test import TestCase, Client

import random

from subscriptions.models import SubscriptionPlan, CurrentSubscription
from accounts.models import Account
from payments.models import PaymentInfo, PaymentHistory

# Create your tests here.
class SubscriptionTest(TestCase):

    def setUp(self):
        # register a user
        self.user = Account.objects.create_user(
            username="test_user",
            email="test@test.com",
            phone_number="+1234567890",
            password="test_password",
        )

        # create a subscription
        self.subscription = [
            SubscriptionPlan.objects.create(
                payment=random.randint(0, 100),
                interval=i,
            )
            for i in ["yearly", "monthly"]
        ]

    def test_create_subscription(self):
        # create a subscription
        subscription = SubscriptionPlan.objects.create(
            payment=10.00,
            interval=random.choice(["monthly", "yearly"]),
        )

        # check if subscription is created
        self.assertTrue(subscription)

    def test_subscribe(self):
        client = Client()
        client.login(username=self.user.username, password="test_password")

        # subscribe to a subscription
        response = client.post(
            "/subscriptions/subscribe/",
            {
                "plan": self.subscription[0].id,
            },
        )

        # should fail because no payment info
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "User does not have Payment Info to subscribe"})
        self.assertFalse(CurrentSubscription.objects.filter(account=self.user).exists())

        # add payment info
        response = client.post(
            "/payments/add/",
            {
                "card_number": "1234567890123456",
                "expiry_date": "2023-12-31",
                "cvv": "123",
                "name_on_card": "test",
            },
        )

        print(response.json())
        self.assertEqual(response.status_code, 201)
        self.assertTrue(PaymentInfo.objects.filter(account=self.user).exists())

        # subscribe to a subscription
        response = client.post(
            "/subscriptions/subscribe/",
            {
                "plan": self.subscription[0].id,
            },
        )

        # should succeed
        self.assertEqual(response.status_code, 201)
        self.assertTrue(CurrentSubscription.objects.filter(account=self.user).exists())
        

        