from cats.models import Breed, Cat, Home, Human
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    humans = serializers.PrimaryKeyRelatedField(many=True, queryset=Human.objects.all())
    cats = serializers.PrimaryKeyRelatedField(many=True, queryset=Cat.objects.all())
    homes = serializers.PrimaryKeyRelatedField(many=True, queryset=Home.objects.all())
    breeds = serializers.PrimaryKeyRelatedField(many=True, queryset=Breed.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'humans', 'cats', 'homes', 'breeds']

class CatSerializer(serializers.ModelSerializer):
	home = serializers.ReadOnlyField(source = 'owner.home.name')

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
	
	class Meta:
		model = Cat
		user = serializers.ReadOnlyField(source = 'user.username')
		fields = ['ID', 'user', 'name', 'gender', 'date_of_birth', 'description', 'breed', 'owner', 'home']


class BreedSerializer(serializers.ModelSerializer):
	cats = CatSerializer(read_only = True, many = True)
	homes = serializers.ReadOnlyField(source='cats.owner.home.name')
	

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
	
	class Meta:
		model = Breed
		user = serializers.ReadOnlyField(source='user.username')
		fields = ['ID', 'user','name', 'origin', 'description', 'cats', 'homes']

class HumanSerializer(serializers.ModelSerializer):
	cats = CatSerializer(read_only=True, many=True)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	class Meta:
		user = serializers.ReadOnlyField(source='user.username')
		model = Human
		fields = ['ID', 'user', 'name', 'gender', 'date_of_birth', 'description', 'home', 'cats']

class HomeSerializer(serializers.ModelSerializer):
	humans = HumanSerializer(read_only = True, many = True)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	class Meta:
		user = serializers.ReadOnlyField(source='user.username')
		model = Home
		fields = ['ID', 'user', 'name', 'address', 'home_type', 'humans']
