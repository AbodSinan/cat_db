from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.authentication import TokenAuthentication

from cats.models import Cat, Home, Human, Breed
from cats.serializers import CatSerializer, HumanSerializer, HomeSerializer, BreedSerializer, UserSerializer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'homes': reverse('home-list', request=request, format=format),
        'cats': reverse('cat-list', request=request, format=format),
        'humans': reverse('human-list', request=request, format=format),
        'breeds': reverse('breed-list', request=request, format=format),
    })

class UserViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	a Viewset to create and track users
	"""
	
	permission_classes = [permissions.IsAdminUser]
	queryset = User.objects.all()
	serializer_class = UserSerializer
	
class CatViewSet(viewsets.ModelViewSet):
	"""
	View to show list of Cats using generic API
	"""

	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	queryset = Cat.objects.all()
	serializer_class = CatSerializer

class BreedViewSet(viewsets.ModelViewSet):
	"""
	View to show list of Breed using generic API
	"""

	permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
	queryset = Breed.objects.all()
	serializer_class = BreedSerializer

class HomeViewSet(viewsets.ModelViewSet):
	"""
	View to show a list of Home using generic API
	"""

	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	queryset = Home.objects.all()
	serializer_class = HomeSerializer

class HumanViewSet(viewsets.ModelViewSet):
	"""
	View to show list of Human using generic API
	"""
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	queryset = Human.objects.all()
	serializer_class = HumanSerializer