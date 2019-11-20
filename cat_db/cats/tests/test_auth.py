from faker import Faker
import datetime
import mock

from django.contrib.auth.models import User, AnonymousUser
from django.conf import settings

from rest_framework import serializers
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate, APIClient
from rest_framework.authtoken.models import Token

from cats.views import BreedViewSet
from cats.factories import BreedFactory
from cats.authentication import is_token_expired
from cats.serializers import BreedSerializer


class FakeDateTime(datetime.datetime):
    """
    overwriting the datetime class to manipulate datetime
    """
    def __new__(cls, *args, **kwargs):
        return datetime.datetime.__new__(datetime, *args, **kwargs)

class UnauthorizedAccessTest(APITestCase):
    """
    Defines test cases for access with or without authorization
    """

    def setUp(self):
        fake = Faker()
        name = fake.name()
        email = fake.email()
        password = fake.pystr()
        self.user = User.objects.create_user(name, email, password) #no need to define token, since the process is automated on object creation in models.py
        self.client.login(username = name, password = password)
        response = self.client.post('/api/token/', {'username' : name, 'password' : password})
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']
        self.data = {'ID' : 37, 'user': self.user.id, 'name': "kwan", 
                    'origin' : "mozambique",'description': "some description", 'cats' : [],
                    'homes' : []}
        
    def test_auth_get(self):
        """
        test an authorized user's get request
        """
        breed = BreedFactory(user=self.user)
        response = self.client.get('/breeds/', HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.assertEqual(response.status_code, 200)
        #validate posted data
        self.assertEqual(response.json()[0], BreedSerializer(instance = breed).data)

    def test_unauth_get(self):
        """
        testing unauthorized person's GET request
        """
        breed = BreedFactory(user=self.user)
        response = self.client.get('/breeds/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0], BreedSerializer(instance = breed).data)

    def test_unauth_post(self):
        """
        testing a non-logged in user's ability to post
        """
        self.client.logout()
        response = self.client.post('/breeds/', self.data, format = 'json')
        self.assertEqual(response.status_code, 403)

    def test_auth_post(self):
        """
        testing client POST request with valid token
        """
        response = self.client.post('/breeds/',self.data, HTTP_AUTHORIZATION='Token ' + self.access_token, format = 'json')
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/breeds/', HTTP_AUTHORIZATION='Token ' + self.access_token)
        self.assertEqual(dict(response.data[0]), self.data)

    @mock.patch('rest_framework_simplejwt.serializers.TokenRefreshSerializer.validate')
    def test_token_expiry(self, expiry_mock):
        """
        testing the expiry of token
        """
        # set the mocked response to return "Refresh has expired"
        expiry_mock.side_effect = serializers.ValidationError('Refresh has expired.')
        #attempt to refresh
        response = self.client.post('/api/token/')
        self.assertEquals(response.status_code, 400)
        #attempt to post
        response = self.client.post('/breeds/')
        self.assertEquals(response.status_code, 400)

    def test_invalid_token(self):
        """
        made a new client with an invalid token
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'abc')
        response = client.post('/breeds/',self.data)
        self.assertEqual(response.status_code, 403)