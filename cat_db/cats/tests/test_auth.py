from faker import Faker
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token

from cats.views import BreedViewSet


class TestAuth(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = BreedViewSet.as_view({'get': 'list'})
        self.uri = '/breeds/'
        self.user = User.objects.create_user(
            username = 'test',
            email='testuser@test.com',
            password='test')

    def test_list(self):
        request = self.factory.get(self.uri,
           HTTP_AUTHORIZATION='Token {}'.format(Token.objects.get(user = self.user)))
        request = self.factory.get(self.uri, HTTP_AUTHORIZATION=None)
        request.user = self.user
        force_authenticate(request, self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))