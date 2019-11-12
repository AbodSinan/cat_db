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
        self.client = APITestCase
        self.client.create_superuser('admin', 'admin@example', 'testing321')
        self.client.login(username = 'admin', password='testing321')
        self.breed_data = {
            'ID' : 1,
            'name' : 'shorthair',
            'origin' : 'Persian',
            'description' : 'short',
        }
        self.breed = Breed.objects.create(**self.breed_data)
        self.serializer = BreedSerializer(instance = self.Breed)
        self.new_data = {
            'ID' : 22,
            'name' : 'longhair',
            'origin' : 'European',
            'description' : 'long',
        }

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertItemsEqual(data.keys(), ['ID', 'user', 'name', 'origin', 'description'])

    def test_contains_correct_description(self):
        data = self.serializer.data
        self.assertEqual(data['description'], self.breed_data['description'])
        
    def test_contains_correct_origin(self):
        data = self.serializer.data
        self.assertEqual(data['origin'], self.breed_data['origin'])
        
    def test_can_change(self):
        self.serializer = BreedSerializer(instance = self.Breed, context = self.new_data)
        self.assertEqual(self.serializer.data['description'], self.new_data['description'])

    def test_can_retrieve(self):
        self.retrieved = self.serializer.get(pk=1)
        self.assertEqual(self.retrieved.data['description'], self.breed_data['description'])
