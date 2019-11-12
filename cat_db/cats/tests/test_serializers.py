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
        self.client.login(username = 'admin', password='testing321')
        self.breed = BreedFactory(pk=self.pk)
        self.serializer = BreedSerializer(instance = self.breed)
        self.new_breed = BreedFactory()

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(data.keys(), set(['ID', 'user', 'name', 'origin', 'description', 'cats', 'homes']))

    def test_contains_correct_description(self):
        data = self.serializer.data
        self.assertEqual(data['description'], self.breed.description)
        
    def test_contains_correct_origin(self):
        data = self.serializer.data
        self.assertEqual(data['origin'], self.breed.origin)
        
    def test_can_change(self):
        self.serializer = BreedSerializer(instance = self.breed, context = BreedFactory())
        self.assertEqual(self.serializer.data['description'], self.new_breed.description)

    def test_can_retrieve(self):
        get_breed = Breed.objects.get(pk = self.pk)
        self.retrieved = BreedSerializer(get_breed)
        self.assertEqual(self.retrieved.data['description'], self.breed.description)
