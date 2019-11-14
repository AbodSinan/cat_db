import factory
from faker import Faker
import coreapi

from django.contrib.auth.models import AnonymousUser, User

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

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
        self.user = User.objects.create_superuser(name, email, password) #no need to define token, since the process is automated on object creation in models.py
        #self.client.auth = TokenAuthentication()
        self.client.login(username = name, password = password)
        print(self.client.isstaff)
        response = self.client.post('/api-auth-token/', {'username' : self.user.username, 'password' : self.user.password}, format='json')
        #request.user = self.user
        #force_authenticate(request, user=self.user)
        #response = obtain_auth_token(request)
        self.access_token = response.json()
        #TODO: figure out how to convert this token into a Token object
        print(response.data)
        self.unauth_user = AnonymousUser()
        self.breed = BreedFactory(user=self.user)
        self.breed_new = BreedFactory(user = self.user)
        self.serial = BreedSerializer(instance = self.breed)
        self.serial_new = BreedSerializer(instance = self.breed_new)
        self.token = Token.objects.get(user=self.user, key=self.access_token)


    def test_auth_get(self):
        request = self.factory.get('/cats/', HTTP_AUTHORIZATION='Token {}'.format(self.token))
        request.user = self.user
        view = CatViewSet.as_view({'get' : 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_unauth_get(self):
        request = self.factory.get('/cats/')
        request.user = self.unauth_user
        view = CatViewSet.as_view({'get' : 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    #TODO:'NoneType' object has no attribute 'split', PROBABLY DUE TO THE HTTP AUTHORIZATION
    def test_unauth_post(self):
        request = self.factory.post('/breeds/', self.serial.data, HTTP_AUTHORIZATION='Token {}'.format(self.token))
        request.user = self.unauth_user
        view = BreedViewSet.as_view({'post' : 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 401)
    #TODO: 'NoneType' object has no attribute 'split'
    def test_auth_post(self):
        request = self.factory.post('/breeds/', self.serial.data, HTTP_AUTHORIZATION='Token {}'.format(self.token))
        request.user = self.user
        view = BreedViewSet.as_view({'post' : 'create'})
        response = view(request, user = self.user, token = self.token)
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
        self.token = Token.objects.get(user=self.user)
        self.unauth_user = AnonymousUser()
        self.breed = BreedFactory()
        self.breed_new = BreedFactory()
        self.serial = BreedSerializer(instance = self.breed)
        self.serial_new = BreedSerializer(instance = self.breed_new)

    def test_breed_getList(self):
        view = BreedViewSet.as_view({'get': 'list'})
        request = self.factory.get('/breeds/')
        force_authenticate(request, user = self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_breed_post(self):
        view = BreedViewSet.as_view({'post': 'create'})
        request = self.factory.post('/breeds/', {'user': self.user, 'name': 'Alexander Turner', 
                                    'origin': 'gUkHwJHaLPUiaQLyDNVu', 'description': 'Indicate camera last raise fill'}, HTTP_AUTHORIZATION='Token {}'.format(self.token))
        force_authenticate(request, user = self.user, token = self.token)
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_breed_retrieve_auth(self):
        """
        test whether an authenticated user can retrieve
        """
        view = BreedViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('/breeds/')
        request.user = self.user
        response = view(request, pk=self.breed.ID)
        self.assertEqual(response.status_code, 200)

    def test_breed_retrieve_unauth(self):
        """
        test whether an unauthenticated user can retrieve
        """
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