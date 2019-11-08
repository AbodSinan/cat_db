import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient, RequestsClient
from rest_framework.authtoken.models import Token

from cats.serializers import HomeSerializer 
from cats.models import Home

"""
class TestCreateHome(APITestCase):
	def setUp(self):
		user = User.objects.create_superuser('admin', 'admin@example.com', 'testing321')
		self.assertTrue(self.client.login(username='admin', password='testing321'))
		self.data = {
		'ID' : 17, 'name' : 'barbados', 'home_type' : 'LD', 'address' : 'safsadgas', 'user' : user.username
		}

	#def test_create_user(self):

	   
	def test_can_add_home(self):
		
		response = self.client.post('/homes/', self.data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
"""

class TestUserAccess(APITestCase):
	def setUp(self):
		self.factory = APIRequestFactory()
		self.client = RequestsClient()

	def test_get_homes(self):
		response = self.client.get('http://testserver/homes/')
		assert response.status_code == 200

	def test_get_cats(self):
		response = self.client.get('http://testserver/cats/')
		assert response.status_code == 200

	def test_get_humans(self):
		response = self.client.get('http://testserver/humans/')
		assert response.status_code == 200

	def test_get_breeds(self):
		response = self.client.get('http://testserver/breeds/')
		assert response.status_code == 200
"""
class TestUserCreate(APITestCase):
	def setUp(self):
		self.user = User.objects.create_superuser('admin', 'admin@example.com', 'testing321')
		self.assertTrue(self.client.login(username='admin', password='testing321'))

	def test_home_create(self):
		data = {'ID' : 1214, 'name' : 'a3rwef', 'address' : '234fasdf', 'home_type': 'LD'}
		response = self.client.post("/homes/", data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
"""