import factory
from faker import Faker

from django.contrib.auth.models import AnonymousUser, User

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate, APIClient

from cats.views import BreedViewSet, CatViewSet, HomeViewSet, HumanViewSet
from cats.models import Cat, Breed
from cats.factories import HomeWithHumans, BreedWithCats, CatFactory, HumanWithCats, BreedFactory
from cats.serializers import BreedSerializer


class UnauthorizedAccessTest(APITestCase):
    """
    Defines test cases for access with or without authorization
    """

    def setUp(self):
        fake = Faker()
        name = fake.name()
        email = fake.email()
        password = fake.pystr()
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(name, email, password)
        self.breed = BreedFactory(user=self.user)
        self.breed_new = BreedFactory(user = self.user)
        self.serial = BreedSerializer(instance = self.breed)
        self.serial_new = BreedSerializer(instance = self.breed_new)
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    def test_auth_get(self):
        request = self.factory.get('/cats/', HTTP_AUTHORIZATION='Token {}'.format(self.token))
        request.user = self.user
        view = CatViewSet.as_view({'get' : 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_unauth_get(self):
        request = self.factory.get('/cats/', HTTP_AUTHORIZATION=None)
        request.user = self.user
        view = CatViewSet.as_view({'get' : 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    #TODO:'NoneType' object has no attribute 'split', PROBABLY DUE TO THE HTTP AUTHORIZATION
    def test_unauth_post(self):
        request = self.factory.post('/breeds/', self.serial.data)
        view = BreedViewSet.as_view({'post' : 'create'})
        response = view(request, user=self.unauth_user)
        self.assertEqual(response.status_code, 401)
    #TODO: 'NoneType' object has no attribute 'split'
    def test_auth_post(self):
        request = self.factory.post('/breeds/', self.serial.data)
        view = BreedViewSet.as_view({'post' : 'create'})
        response = view(request, user=self.user)
        self.assertEqual(response.status_code, 200)

class CRETViewTests(APITestCase):
    """
    Tests for the Creation, deletion, retrieval, and update from views
    """

    def setUp(self):
        fake = Faker()
        name = fake.name()
        email = fake.email()
        password = fake.pystr()
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(name, email, password)
        self.unauth_user = AnonymousUser()
        self.breed = BreedFactory()
        self.breed_new = BreedFactory()
        self.serial = BreedSerializer(instance = self.breed)
        self.serial_new = BreedSerializer(instance = self.breed_new)

    def test_breed_getList(self):
        view = BreedViewSet.as_view({'get': 'list'})
        request = self.factory.get('/breeds/')
        force_authenticate(request, user = self.breed.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_breed_post(self):
        view = BreedViewSet.as_view({'post': 'create'})
        request = self.factory.post('/breeds/', self.serial.data    )
        force_authenticate(request, user = self.breed.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_breed_retrieve(self):
        view = BreedViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('/breeds/')
        request.user = self.unauth_user
        response = view(request, pk=self.breed.ID)
        self.assertEqual(response.status_code, 200)

    def test_breed_put(self):
        view = BreedViewSet.as_view({'put': 'update'})
        request = self.factory.put('/breeds/'  + str(self.breed.ID) + '/', data=self.serial_new.data)
        force_authenticate(request, user = self.user)
        response = view(request, pk=self.breed.ID)
        self.assertEqual(response.status_code, 200)

    def test_breed_delete(self):
        view = BreedViewSet.as_view({'delete' : 'destroy'})
        request = self.factory.delete('/breeds/' + str(self.breed.ID) + '/')
        force_authenticate(request, user = self.user)
        response = view(request,pk=self.breed.ID)
        self.assertEqual(response.status_code, 204)