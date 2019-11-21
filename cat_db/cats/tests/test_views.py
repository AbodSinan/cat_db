import factory
from faker import Faker
import coreapi
import datetime

from django.contrib.auth.models import AnonymousUser, User
from django.conf import settings
from django.forms.models import model_to_dict

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from cats.views import BreedViewSet, CatViewSet, HomeViewSet, HumanViewSet
from cats.models import Cat, Breed
from cats.factories import HomeWithHumans, BreedWithCats, CatFactory, HumanWithCats, BreedFactory, HomeFactory, HumanFactory
from cats.serializers import BreedSerializer, HomeSerializer, HumanSerializer, CatSerializer
from cats.authentication import is_token_expired, expires_in


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
        self.breed_data = {
            'ID' : 1, 'name' : 'grayhound', 'origin' : 'siberia',
            'description' : 'just a dog', 'user' : self.user.id
        }
        self.home_data = {
            'ID' : 1, 'name' : 'sfda', 'address' : 'home',
            'home_type' : "CD", 'user' : self.user.id
        }
        self.human_data = {
            'ID' : 1,'user' :self.user.id, 'name' : 'sofia', 'gender' : 'male', 'date_of_birth' : '1996-12-19',
            'description' : 'some description', 'cats' : []
        }
        self.cat_data = {
            'ID' : 1, 'name' : 'snuffles', 'gender' : 'neuter',
            'user' : self.user.id,'date_of_birth' : '1996-12-19',
            'description' : 'some description'
        }

    def test_breed_getList(self):
        """
        test whether a user can retrieve a list of breed objects
        """
        breed1 = BreedFactory(user = self.user)
        breed2 = BreedFactory(user = self.user)
        view = BreedViewSet.as_view({'get': 'list'})
        request = self.factory.get('/breeds/')
        force_authenticate(request, user = self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([dict(x) for x in response.data], 
                        [BreedSerializer(instance = breed1).data,
                         BreedSerializer(instance = breed2).data])

    def test_breed_post(self):
        """
        test whether a user can post data into breeds
        """
        data = self.breed_data
        view = BreedViewSet.as_view({'post': 'create', 'get' : 'retrieve'})
        request = self.factory.post('/breeds/', data)
        force_authenticate(request, user = self.user)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        request = self.factory.get('/breeds/')
        force_authenticate(request, user = self.user)
        response = view(request, pk=data['ID'])
        data['homes'] = []
        data['cats'] = []
        self.assertEqual(response.data, data)

    def test_breed_retrieve_auth(self):
        """
        test whether an authenticated user can retrieve
        """
        breed = BreedFactory(user = self.user)
        view = BreedViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('/breeds/')
        request.user = self.user
        force_authenticate(request, user = self.user)
        response = view(request, pk=breed.ID)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, BreedSerializer(instance = breed).data)

    def test_breed_retrieve_unauth(self):
        """
        test whether an unauthenticated user can retrieve
        """
        breed = BreedFactory(user = self.user)
        view = BreedViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('/breeds/')
        request.user = self.unauth_user
        response = view(request, pk=breed.ID)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, BreedSerializer(instance = breed).data)

    def test_breed_put(self):
        """
        test whether a user can update a Breed instance
        """
        breed = BreedFactory(user = self.user)
        data = self.breed_data
        data['cats'] = []
        data['name'] = 'dandelion'
        view = BreedViewSet.as_view({'put': 'update'})
        request = self.factory.put('/breeds/', data)
        force_authenticate(request, user = self.user)
        response = view(request, pk=breed.ID)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'dandelion')

    def test_breed_delete(self):
        """
        test if a user can delete a Breed instance
        """
        breed = BreedFactory(user = self.user)
        view = BreedViewSet.as_view({'delete' : 'destroy'})
        request = self.factory.delete('/breeds/' + str(breed.ID) + '/')
        force_authenticate(request, user = self.user)
        response = view(request,pk=breed.ID)
        self.assertEqual(response.status_code, 204)

    def test_home_getList(self):
        """
        test if a user can get a list of Home objects
        """
        home1 = HomeFactory(user = self.user)
        serial1 = HomeSerializer(instance = home1).data
        home2 = HomeFactory(user = self.user)
        serial2 = HomeSerializer(instance = home2).data
        view = HomeViewSet.as_view({'get': 'list'})
        request = self.factory.get('/homes/')
        force_authenticate(request, user = self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([dict(x) for x in response.data],
                        [serial1, serial2])

    def test_home_post(self):
        """
        test if a user can post a Home object
        """
        view = HomeViewSet.as_view({'post': 'create'})
        request = self.factory.post('/homes/', self.home_data)
        force_authenticate(request, user = self.user)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, self.home_data)

    def test_home_retrieve_auth(self):
        """
        test whether an authenticated user can retrieve
        """
        home = HomeFactory(user = self.user)
        view = HomeViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('/breeds/')
        request.user = self.user
        force_authenticate(request, user = self.user)
        response = view(request, pk=home.ID)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, HomeSerializer(instance = home).data)

    def test_home_retrieve_unauth(self):
        """
        test whether an unauthenticated user can retrieve a Home object
        """
        home = HomeFactory(user = self.user)
        view = HomeViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('/homes/')
        response = view(request, pk=home.ID)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, HomeSerializer(instance = home).data)

    def test_home_put(self):
        """
        test whether a user can update a Home instance
        """
        home = HomeFactory(user = self.user)
        home_serial = HomeSerializer(home).data
        home_serial['name'] = 'jones'
        view = HomeViewSet.as_view({'put': 'update'})
        request = self.factory.put('/homes/', home_serial)
        force_authenticate(request, user = self.user)
        response = view(request, pk=home.ID)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'jones') 

    def test_home_delete(self):
        """
        tests whether the user can delete a Home instance
        """
        home = HomeFactory(user = self.user)
        view = HomeViewSet.as_view({'delete' : 'destroy'})
        request = self.factory.delete('/homes/' + str(home.ID) + '/')
        force_authenticate(request, user = self.user)
        response = view(request,pk=home.ID)
        self.assertEqual(response.status_code, 204)


    def test_human_getList(self):
        """
        tests whether a user can get a list of Human objects
        """
        human1 = HumanFactory(user = self.user)
        human2 = HumanFactory(user = self.user)
        view = HumanViewSet.as_view({'get' : 'list'})
        request = self.factory.get('/humans/')
        request.user = self.user
        force_authenticate(request, user = self.user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([dict(x) for x in response.data], 
                        [HumanSerializer(instance = human1).data,
                         HumanSerializer(instance = human2).data])

    def test_human_post(self):
        """
        tests whether a user can post an instance of Human
        """
        home = HomeFactory(user = self.user)
        data = self.human_data
        data['home'] = home.ID
        view = HumanViewSet.as_view({'post' : 'create'})
        request = self.factory.post('/humans/', data)
        force_authenticate(request, user = self.user)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, data)

    def test_human_delete(self):
        """
        tests whether a user can delete an instance of Human
        """
        human = HumanFactory(user = self.user)
        view = HumanViewSet.as_view({'delete' : 'destroy'})
        request = self.factory.delete('/humans/' + str(human.ID) + '/')
        force_authenticate(request, user = self.user)
        response = view(request, pk = human.ID)
        self.assertEqual(response.status_code, 204)

    def test_human_put(self):
        """
        tests whether a user can update an instance of Human
        """
        home = HomeFactory(user = self.user)
        human = HumanFactory(user = self.user)
        view = HumanViewSet.as_view({'put' : 'partial_update'})
        data = self.human_data
        data['user'] = self.user.id
        data['home'] = home.ID
        data['gender'] = 'fallic'
        request = self.factory.put('/humans/', data)
        force_authenticate(request, user=self.user)
        response = view(request, pk=human.ID)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['gender'], 'fallic')

    def test_cat_getList(self):
        """
        tests whether the user can get a list of Cat objects
        """
        breed = BreedFactory(user = self.user)
        home = HomeFactory(user = self.user)
        owner = HumanFactory(user = self.user, home = home)
        cat1 = CatFactory(user = self.user, breed = breed, owner = owner)
        cat2 = CatFactory(user = self.user, breed = breed, owner = owner)
        view = CatViewSet.as_view({'get' : 'list'})
        request = self.factory.get('/cats/')
        force_authenticate(request)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        cat1_serial = CatSerializer(instance = cat1).data
        cat1_serial['home'] = home.name
        cat2_serial = CatSerializer(instance = cat2).data
        cat2_serial['home'] = home.name
        self.assertEqual([dict(x) for x in response.data], [cat1_serial, cat2_serial])

    def test_cat_post(self):
        """
        tests whether the user can post a Cat object
        """
        home = HomeFactory(user = self.user)
        breed = BreedFactory(user = self.user)
        owner = HumanFactory(user = self.user, home = home)
        data = self.cat_data
        data['breed'] = breed.ID
        data['owner'] = owner.ID
        data['home'] = home.ID
        view = CatViewSet.as_view({'post' : 'create'})
        request = self.factory.post('/cats/', data)
        force_authenticate(request, user = self.user)
        response = view(request)
        data['home'] = home.name
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, data)

    def test_cat_delete(self):
        """
        tests whether the user can delete a Cat object using a view
        """
        cat = CatFactory(user = self.user)
        view = CatViewSet.as_view({'delete' : 'destroy'})
        request = self.factory.delete('/cats/' + str(cat.ID) + '/')
        force_authenticate(request, user = self.user)
        response = view(request, pk = cat.ID)
        self.assertEqual(response.status_code, 204)
        