from django.contrib.auth.models import User

from rest_framework import serializers

from cats.models import Breed, Cat, Human, Home

class UserSerializer(serializers.ModelSerializer):
    humans = serializers.PrimaryKeyRelatedField(many=True, queryset=Human.objects.all())
    cats = serializers.PrimaryKeyRelatedField(many=True, queryset=Cat.objects.all())
    homes = serializers.PrimaryKeyRelatedField(many=True, queryset=Home.objects.all())
    breeds = serializers.PrimaryKeyRelatedField(many=True, queryset=Breed.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'humans', 'cats', 'homes', 'breeds']

class CatSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cat
		user = serializers.ReadOnlyField(source = 'user.username')
		home = serializers.ReadOnlyField(source = 'owner.home')
		fields = ('ID', 'user', 'name', 'gender', 'date_of_birth', 'description', 'breed', 'owner' ,'home',)


class BreedSerializer(serializers.ModelSerializer):
	class Meta:
		model = Breed
		user = serializers.ReadOnlyField(source='user.username')
		cats = CatSerializer(read_only = True, many = True)
		fields = ['ID', 'user','name', 'origin', 'description', 'homes', 'cats', 'homes']

class HumanSerializer(serializers.ModelSerializer):
	class Meta:
		user = serializers.ReadOnlyField(source='user.username')
		model = Human
		cats = CatSerializer(read_only=True, many=True)
		fields = ['ID', 'user', 'name', 'gender', 'date_of_birth', 'description', 'home', 'cats']

class HomeSerializer(serializers.ModelSerializer):
	class Meta:
		user = serializers.ReadOnlyField(source='user.username')
		humans = HumanSerializer(read_only = True, many = True)
		model = Home
		fields = ['ID', 'user', 'name', 'address', 'home_type']