import datetime

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)

from cats.models import Cat, Home, Human, Breed
from cats.serializers import CatSerializer, HumanSerializer, HomeSerializer, BreedSerializer, UserSerializer, UserSigninSerializer
from cats.authentication import token_expire_handler, expires_in

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'homes': reverse('home-list', request=request, format=format),
        'cats': reverse('cat-list', request=request, format=format),
        'humans': reverse('human-list', request=request, format=format),
        'breeds': reverse('breed-list', request=request, format=format),
    })

@api_view(["POST"])
@permission_classes((permissions.AllowAny, ))
def signin(request):
    signin_serializer = UserSigninSerializer(data = request.data)
    if not signin_serializer.is_valid():
        return Response(signin_serializer.errors, status = HTTP_400_BAD_REQUEST)


    user = authenticate(
            username = signin_serializer.data['username'],
            password = signin_serializer.data['password'] 
        )
    if not user:
        return Response({'detail': 'Invalid Credentials or activate account'}, status=HTTP_404_NOT_FOUND)
        
    #TOKEN STUFF
    token, _ = Token.objects.get_or_create(user = user)
    
    #token_expire_handler will check, if the token is expired it will generate new one
    is_expired, token = token_expire_handler(token)     # The implementation will be described further
    user_serialized = UserSerializer(user)

    return Response({
        'user': user_serialized.data, 
        'expires_in': expires_in(token),
        'token': token.key
    }, status=HTTP_200_OK)

"""
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
			'time_created' : created
        })
"""

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