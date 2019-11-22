from faker import Faker
import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from rest_framework.test import APITestCase, APIClient

from cats.models import Cat, Home, Breed, Human
from cats.serializers import BreedSerializer, HumanSerializer
from cats.factories import HumanWithCats, BreedFactory, HumanFactory, CatFactory, HomeFactory

class TestHomeModel(APITestCase):
    """
    Defines tests for validation of requests using APIClient
    """
    def setUp(self):
        #self.client.create_superuser('admin', 'admin@example', 'testing321')
        fake = Faker()
        self.pk = fake.pyint()
        username = fake.name()
        password = fake.pystr()
        self.user = User.objects.create_user(username, password)
        self.client.login(username = username, password=password)

    def test_birthdate_validator(self):
        """
        test to validate the date_of_birth field
        """
        human = HumanFactory( date_of_birth= datetime.date.today() + datetime.timedelta(days=5))
        serial = HumanSerializer(data= human)
        self.assertEqual(serial.is_valid(), False)

    def test_serializer_post(self):
        breed = BreedFactory(user = self.user)
        retrieved = Breed.objects.get(ID = breed.ID)
        self.assertEqual(retrieved, breed)

    def test_serializer_delete(self):
        breed = BreedFactory(user = self.user)
        Breed.objects.get(ID = breed.ID).delete()
        with self.assertRaises(ObjectDoesNotExist):
            Breed.objects.get(ID=breed.ID)

    def test_serializer_change(self):
        fake = Faker()
        breed = BreedFactory(user = self.user)
        retrieved = Breed.objects.get(ID = breed.ID)
        retrieved.origin = fake.pystr()
        retrieved.save()
        new = Breed.objects.get(ID = breed.ID)
        self.assertEqual(new.origin, retrieved.origin)
        