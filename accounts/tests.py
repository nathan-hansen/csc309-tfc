import random

from django.test import TestCase


# Create your tests here.
class AccountTestCase(TestCase):
    username = 'test' + str(random.randint(1, 100000))
    password = '123'

    def register_and_sign_in(self):
        response = self.client.post('/accounts/signup/', {'username': self.username, 'password': self.password, 'password2': self.password})
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/accounts/login/', {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        # without any data
        response = self.client.post('/accounts/signup/')
        self.assertEqual(response.status_code, 400)
        # without username
        response = self.client.post('/accounts/signup/', {'password': '123', 'password2': '123'})
        self.assertEqual(response.status_code, 400)
        # without password
        response = self.client.post('/accounts/signup/', {'username': 'test', 'password2': '123'})
        self.assertEqual(response.status_code, 400)
        # without password2
        response = self.client.post('/accounts/signup/', {'username': 'test', 'password': '123'})
        self.assertEqual(response.status_code, 400)
        # password and password2 do not match
        response = self.client.post('/accounts/signup/', {'username': 'test', 'password': '123', 'password2': '1234'})
        self.assertEqual(response.status_code, 400)
        
        # successful signup
        response = self.client.post('/accounts/signup/', {'username': self.username, 'password': self.password, 'password2': self.password})
        self.assertEqual(response.status_code, 201)
        # username already exists
        response = self.client.post('/accounts/signup/', {'test': self.username, 'password': self.password, 'password2': self.password})
        self.assertEqual(response.status_code, 400)


    def test_login(self):
        # successful signup
        response = self.client.post('/accounts/signup/', {'username': self.username, 'password': self.password, 'password2': self.password})
        self.assertEqual(response.status_code, 201)
        # without username
        response = self.client.post('/accounts/login/', {'password': '123'})
        self.assertEqual(response.status_code, 400)
        # without password
        response = self.client.post('/accounts/login/', {'username': 'test'})
        self.assertEqual(response.status_code, 400)
        # user does not exist
        response = self.client.post('/accounts/login/', {'username': 'test' + str(random.randint(1, 100000)), 'password': '123'})
        self.assertEqual(response.status_code, 401)
        # wrong password
        response = self.client.post('/accounts/login/', {'username': self.username, 'password': '1234'})
        self.assertEqual(response.status_code, 401)

        # successful login
        response = self.client.post('/accounts/login/', {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_refresh(self):
        self.register_and_sign_in()
        # without refresh token
        response = self.client.post('/accounts/api/token/refresh/')
        self.assertEqual(response.status_code, 400)

        # successful refresh
        response = self.client.post('/accounts/login/', {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)
        refresh_token = response.data['refresh']
        response = self.client.post('/accounts/api/token/refresh/', {'refresh': refresh_token})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.data)
        self.assertTrue(response.data['access'] != refresh_token)


    def test_update(self):
        self.register_and_sign_in()
        # without access token
        response = self.client.post('/accounts/update/', {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 401)

        # successful update
        response = self.client.post('/accounts/login/', {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)
        access_token = response.data['access']

        avatar = open('./tests/wojak.jpg', 'rb')
        response = self.client.put('/accounts/update/', {
            'username': self.username,
            'password': self.password,
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@test.com',
            'phone': '1234567890',
            'avatar': avatar
            }, HTTP_AUTHORIZATION='Bearer ' + access_token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], self.username)
        self.assertEqual(response.data['first_name'], 'test')
        self.assertEqual(response.data['last_name'], 'test')
        self.assertEqual(response.data['email'], 'test@test.com')
        self.assertEqual(response.data['phone'], '1234567890')
        self.assertTrue('avatar' in response.data)
        avatar.close()

