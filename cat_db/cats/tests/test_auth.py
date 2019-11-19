from faker import Faker
import datetime
from mock import patch

from django.contrib.auth.models import User, AnonymousUser
from django.conf import settings

from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory, force_authenticate
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
        response = self.client.post('/api-auth-token/', {'username' : name, 'password' : password})
        self.access_token = response.json()['token']
        self.unauth_user = AnonymousUser()
        self.token = Token.objects.get(user=self.user, key=self.access_token)
        self.data = {'ID' : 37, 'user': self.user.id, 'name': "kwan", 
                    'origin' : "mozambique",'description': "some description", 'cats' : [],
                    'homes' : []}
        
    def test_auth_get(self):
        breed = BreedFactory(user=self.user)
        response = self.client.get('/breeds/', HTTP_AUTHORIZATION='Token {}'.format(self.token))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0], BreedSerializer(instance = breed).data)

    def test_unauth_get(self):
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
        response = self.client.post('/breeds/',self.data, HTTP_AUTHORIZATION='Token {}'.format(self.token), format = 'json')
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/breeds/', HTTP_AUTHORIZATION='Token {}'.format(self.token))
        self.assertEqual(dict(response.data[0]), self.data)

    """
    @patch('cats.authentication.datetime', FakeDateTime) #instead of using the datetime class, use the custom FakeDateTime to simulate future
    def test_expired_token(self):
        FakeDateTime.utcnow = classmethod(lambda cls: datetime.datetime.utcnow() + datetime.timedelta(days =2))
        print(FakeDateTime.utcnow())
        print(is_token_expired(self.token))
        #post with the expired token
        response = self.client.post('/breeds/', self.data, HTTP_AUTHORIZATION='Token {}'.format(self.token))
        print(is_token_expired(self.token))
        self.assertEqual(response.status_code, 403)
    """

    def test_invalid_token(self):
        response = self.client.post('/breeds/',self.data, HTTP_AUTHORIZATION='Token 423134122134')
        print(response.data)
        self.assertEqual(response.status_code, 403)