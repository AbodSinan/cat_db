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
from cats.factories import HomeWithHumans, BreedWithCats, CatFactory, HumanWithCats, BreedFactory, HomeFactory
from cats.serializers import BreedSerializer, HomeSerializer


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
        #self.client.auth = TokenAuthentication()
        self.client.login(username = name, password = password)
        response = self.client.post('/api-auth-token/', {'username' : name, 'password' : password}, format='json')
        #response = obtain_auth_token(request)
        self.access_token = response.json()['token']
        #TODO: figure out how to convert this token into a Token object
        self.unauth_user = AnonymousUser()
        self.breed = BreedFactory(user=self.user)
        self.breed_new = BreedFactory(user = self.user)
        self.serial = BreedSerializer(instance = self.breed)
        self.serial_new = BreedSerializer(instance = self.breed_new)
        self.token = Token.objects.get(user=self.user, key=self.access_token)


    def test_auth_get(self):
        response = self.client.get('/cats/', HTTP_AUTHORIZATION='Token {}'.format(self.token))
        #view = CatViewSet.as_view({'get' : 'list'})
        #response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_unauth_get(self):
        response = self.client.get('/cats/')
        #request.user = self.unauth_user
        #view = CatViewSet.as_view({'get' : 'list'})
        #response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_unauth_post(self):
        """
        testing a non-logged in user's ability to post
        """

        self.client.logout()
        response = self.client.post('/breeds/', {'ID' : 1, 'user': self.user.id, 'name': self.serial.data['name'], 
                                    'origin' : self.serial.data['origin'], 'description': self.serial.data['description']})
        #request.user = self.unauth_user
        #view = BreedViewSet.as_view({'post' : 'create'})
        #response = view(request)
        self.assertEqual(response.status_code, 403)
    #TODO: 'NoneType' object has no attribute 'split'
    def test_auth_post(self):
        response = self.client.post('/breeds/', {'ID' : 1, 'user': self.user.id, 'name': self.serial.data['name'], 
                                    'origin' : self.serial.data['origin'], 'description': self.serial.data['description']}, HTTP_AUTHORIZATION='Token {}'.format(self.token), format = 'json')
        #request.user = self.user
        #view = BreedViewSet.as_view({'post' : 'create'})
        #response = view(request, user = self.user, token = self.token)
        self.assertEqual(response.status_code, 201)
#TODO: ADD MORE TESTS
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
        self.breed = BreedFactory(user = self.user)
        self.breed_new = BreedFactory(user = self.user)
        self.breed_serial = BreedSerializer(instance = self.breed)
        self.serial_new = BreedSerializer(instance = self.breed_new)
        self.home = HomeFactory(user = self.user)
        self.home_new = HomeFactory(user = self.user)
        self.home_serial = HomeSerializer(instance = self.home)

    def test_breed_getList(self):
        view = BreedViewSet.as_view({'get': 'list'})
        request = self.factory.get('/breeds/')
        force_authenticate(request, user = self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_breed_post(self):
        view = BreedViewSet.as_view({'post': 'create'})
        request = self.factory.post('/breeds/', {'ID' : 1, 'user': self.user.id, 'name': self.breed_serial.data['name'], 
                                    'origin' : self.breed_serial.data['origin'], 'description': self.breed_serial.data['description']}, format='json')
        force_authenticate(request, user = self.user)
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_breed_retrieve_auth(self):
        """
        test whether an authenticated user can retrieve
        """
        view = BreedViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('/breeds/')
        request.user = self.user
        force_authenticate(request, user = self.user)
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
        request = self.factory.put('/breeds/', {'ID' : 1, 'user': self.user.id, 'name': self.breed_serial.data['name'], 
                                    'origin' : self.breed_serial.data['origin'], 'description': self.breed_serial.data['description']}, format = 'json')
        force_authenticate(request, user = self.user)
        response = view(request, pk=self.breed.ID)
        self.assertEqual(response.status_code, 200)

    def test_breed_delete(self):
        view = BreedViewSet.as_view({'delete' : 'destroy'})
        request = self.factory.delete('/breeds/' + str(self.breed.ID) + '/')
        force_authenticate(request, user = self.user)
        response = view(request,pk=self.breed.ID)
        self.assertEqual(response.status_code, 204)

    def test_home_getList(self):
        view = HomeViewSet.as_view({'get': 'list'})
        request = self.factory.get('/homes/')
        force_authenticate(request, user = self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_home_post(self):
        view = BreedViewSet.as_view({'post': 'create'})
        print(self.home_serial.data)
        request = self.factory.post('/homes/', self.home_serial.data, format='json')
        force_authenticate(request, user = self.user)
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_home_retrieve_auth(self):
        """
        test whether an authenticated user can retrieve
        """
        view = BreedViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('/breeds/')
        request.user = self.user
        force_authenticate(request, user = self.user)
        response = view(request, pk=self.breed.ID)
        self.assertEqual(response.status_code, 200)

    def test_home_retrieve_unauth(self):
        """
        test whether an unauthenticated user can retrieve
        """
        view = BreedViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('/homes/')
        response = view(request, pk=self.breed.ID)
        self.assertEqual(response.status_code, 200)

    def test_home_put(self):
        view = BreedViewSet.as_view({'put': 'update'})
        request = self.factory.put('/homes/', {'ID' : 2, 'user': self.user.id, 'name': self.home_serial.data['name'], 
                                    'home_type' : self.home_serial.data['home_type'], 'address': self.home_serial.data['address']}, format='json')
        force_authenticate(request, user = self.user)
        response = view(request, pk=self.breed.ID)
        self.assertEqual(response.status_code, 201)

    def test_home_delete(self):
        view = BreedViewSet.as_view({'delete' : 'destroy'})
        request = self.factory.delete('/homes/' + str(self.home.ID) + '/')
        force_authenticate(request, user = self.user)
        response = view(request,pk=self.breed.ID)
        self.assertEqual(response.status_code, 204)