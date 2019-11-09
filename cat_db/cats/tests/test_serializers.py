from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.test import APITestCase, APIClient

from cats.models import Cat, Home, Breed, Human
from cats.serializers import BreedSerializer

class TestHomeModel(APITestCase):
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

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertItemsEqual(data.keys(), ['ID', 'user', 'name', 'origin', 'description'])