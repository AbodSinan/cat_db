import faker, factory

from django.contrib.auth.models import User, AnonymousUser

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate, APIClient

from cats.views import BreedViewSet, CatViewSet, HomeViewSet, HumanViewSet
from cats.models import Cat, Breed
from cats.factories import HomeWithHumans, BreedWithCats, CatFactory, HumanWithCats


class UnauthorizedAccessTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user('noadmin', 'noadmin@example.net', 'testing321')
        self.unauth_user = AnonymousUser()
        self.token = Token.objects.create(user = self.user)
        self.breed_data = {
            'ID' : 1,
            'origin' : 'plantasia',
            'description' : 'a book',
            'name' : 'hoobastank',
        }
        self.breed = Breed.objects.create(**self.breed_data)

        self.token.save()

    def test_auth_get(self):
        request = self.factory.get('/cats', HTTP_AUTHORIZATION='Token {}'.format(self.token))
        force_authenticate(request, user = self.user)
        view = CatViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_unauth_post(self):
        self.client.login(user=self.unauth_user)
        response = self.client.post('/breeds', data = self.breed_data, HTTP_AUTHORIZATION=None)
        self.assertEqual(response.status_code, 401)

    def test_auth_post(self):
        self.client.login(user=self.user)
        response = self.client.post('/breeds', data = self.breed_data, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)

class CRETViewTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory
        self.user = User.objects.get('admin')
        self.unauth_user = AnonymousUser()

        self.breed_data = {
            'ID' : 1,
            'origin' : 'plantasia',
            'description' : 'a book',
            'name' : 'hoobastank',
        }
        
        self.breed_data_new = {
            'ID' : 1,
            'origin' : 'eastasia',
            'description' : 'a book',
            'name' : 'hoobastank',
        }

    def test_breed_post(self):
        view = BreedViewSet.as_view()
        request = self.factory.post('/breeds/', data=self.breed_data)
        force_authenticate(request, user = self.user)
        response = view(request)
        self.assertEqual(response.data['description'], 'a book')

    def test_breed_retrieve(self):
        view = BreedViewSet.as_view()
        request = self.factory.get('/breeds/')
        request.user = self.unauth_user
        response = view(request)
        self.assertEqual(response.data['description'], 'a book')

    def test_breed_put(self):
        view = BreedViewSet.as_view()
        request = self.factory.post('/breeds/', data=self.breed_data_new)
        force_authenticate(request, user = self.user)
        response = view(request)
        self.assertEqual(response.data['origin'], 'eastasia')

    def test_breed_delete(self):
        view = BreedViewSet.as_view()
        request = self.factory.post('/breeds/', data=self.breed_data_new)
        force_authenticate(request, user = self.user)
        response = view(request)