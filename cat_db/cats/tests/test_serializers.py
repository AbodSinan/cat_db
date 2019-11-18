from faker import Faker

from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.test import APITestCase, APIClient

from cats.models import Cat, Home, Breed, Human
from cats.serializers import BreedSerializer
from cats.factories import HumanWithCats, BreedFactory, HumanFactory, CatFactory, HomeFactory

class TestHomeModel(APITestCase):
    """
    Defines tests for the Home Model
    """
    def setUp(self):
        #self.client.create_superuser('admin', 'admin@example', 'testing321')
        fake = Faker()
        self.pk = fake.pyint()
        username = fake.name()
        password = fake.pystr()
        self.user = User.objects.create_user(username, password)
        self.client.login(username = username, password=password)
        self.breed = BreedFactory(user = self.user)
        self.serializer = BreedSerializer(instance = self.breed)
        self.new_breed = BreedFactory()
        print(self.breed._meta.get_fields())

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(data.keys(), set(['ID', 'user', 'name', 'origin', 'description', 'cats', 'homes']))

    def test_contains_correct_data(self):
        retrieved = Breed.objects.get(ID = self.breed.ID)
        self.assertEqual()
        
    def test_can_change(self):
        self.serializer = BreedSerializer(instance = self.breed, context = BreedFactory())
        self.assertEqual(self.serializer.data['description'], self.new_breed.description)
