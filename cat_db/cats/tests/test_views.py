import factory
from faker import Faker

from django.contrib.auth.models import User, AnonymousUser

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate, APIClient

from cats.views import BreedViewSet, CatViewSet, HomeViewSet, HumanViewSet
from cats.models import Cat, Breed
from cats.factories import HomeWithHumans, BreedWithCats, CatFactory, HumanWithCats, BreedFactory


class UnauthorizedAccessTest(APITestCase):
    """
    Defines test cases for access with or without authorization
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user('noadmin', 'noadmin@example.net', 'testing321')
        self.unauth_user = AnonymousUser()
        self.token = Token.objects.create(user = self.user)
        self.breed = BreedFactory

        self.token.save()

    def test_auth_get(self):
        request = self.factory.get('/cats', HTTP_AUTHORIZATION='Token {}'.format(self.token))
        force_authenticate(request, user = self.user)
        view = CatViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_unauth_post(self):
        self.client.login(user=self.unauth_user)
        response = self.client.post('/breeds', data = self.breed.data, HTTP_AUTHORIZATION=None)
        self.assertEqual(response.status_code, 401)

    def test_auth_post(self):
        self.client.login(user=self.user)
        response = self.client.post('/breeds', data = self.breed.data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)

class CRETViewTests(APITestCase):
    """
    Tests for the Creation, deletion, retrieval, and update from views
    """

    def setUp(self):
        self.factory = APIRequestFactory
        self.user = User.objects.get('admin')
        self.unauth_user = AnonymousUser()
        self.breed = BreedFactory()
        self.breed_new = BreedFactory()

    def test_breed_post(self):
        fake = Faker()
        description = fake.text()
        view = BreedViewSet.as_view()
        request = self.factory.post('/breeds/', data=self.breed.data)
        force_authenticate(request, user = self.user)
        response = view(request)
        self.assertEqual(response.data['description'], description)

    def test_breed_retrieve(self):
        fake = Faker()
        description = fake.text()
        view = BreedViewSet.as_view()
        request = self.factory.get('/breeds/')
        request.user = self.unauth_user
        response = view(request)
        self.assertEqual(response.data['description'], description)

    def test_breed_put(self):
        fake = Faker()
        origin = fake.name()
        view = BreedViewSet.as_view()
        request = self.factory.post('/breeds/', data=self.breed_new.data)
        force_authenticate(request, user = self.user)
        response = view(request)
        self.assertEqual(response.data['origin'], origin)

    def test_breed_delete(self):
        view = BreedViewSet.as_view()
        request = self.factory.delete('/breeds/')
        force_authenticate(request, user = self.user)
        response = view(request)
        self.assertEqual(response.status)