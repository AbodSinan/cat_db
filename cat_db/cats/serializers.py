import datetime

from django.contrib.auth.models import User

from rest_framework import serializers

from cats.models import Breed, Cat, Home, Human


class UserSerializer(serializers.ModelSerializer):
	humans = serializers.PrimaryKeyRelatedField(many=True, queryset=Human.objects.all())
	cats = serializers.PrimaryKeyRelatedField(many=True, queryset=Cat.objects.all())
	homes = serializers.PrimaryKeyRelatedField(many=True, queryset=Home.objects.all())
	breeds = serializers.PrimaryKeyRelatedField(many=True, queryset=Breed.objects.all())

	class Meta:
		model = User
		fields = ['id', 'username','password', 'humans', 'cats', 'homes', 'breeds']
		extra_kwargs = {'password' : {'write_only' : True}}
		

	def create(self,validated_data):
		user = User(
			email = validated_data['email'],
			username = validated_data['username']
		)
		user.set_password(validated_data['password'])
		user.save()
		return user

class UserSigninSerializer(serializers.Serializer):
	username = serializers.CharField(required = True)
	password = serializers.CharField(required = True)

class CatSerializer(serializers.ModelSerializer):
	"""
	Serializer of the Human Model
	"""
	
	home = serializers.ReadOnlyField(source = 'owner.home.name')

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
	
	def validate_date_of_birth(self, value):
		if value > datetime.datetime.now():
			raise serializers.ValidationError("Date is in the future")
		return value

	class Meta:
		model = Cat
		user = serializers.ReadOnlyField(source = 'user.username')
		fields = ['ID', 'user', 'name', 'gender', 'date_of_birth', 'description', 'breed', 'owner', 'home']

class HomeListingField(serializers.RelatedField):
	def to_native(self, value):
		return value.home 

class BreedSerializer(serializers.ModelSerializer):
	"""
	Serializer of the Human Model
	"""

	cats = CatSerializer(read_only = True, many = True)
	#homes = HomeListingField(many = True, read_only = True)
	#homes = serializers.ReadOnlyField(source='cats.home')
	#homes = serializers.PrimaryKeyRelatedField(many = True, queryset = cats)
	#homes = serializers.CharField(source='cats.home', read_only=True, many=True) ##many is not included
	#homes = serializers.SlugRelatedField(source = 'cats.all', slug_field='home',many=True, read_only=True)
	homes = serializers.SerializerMethodField()

	def validate_date_of_birth(self, value):
		if value > datetime.datetime.now():
			raise serializers.ValidationError("Date is in the future")
		return value

	def get_homes(self, instance):
		homes = []
		cat_instances =  instance.cats.all()
		for cat in cat_instances:
			homes.append(cat.owner.home.name)
		return homes

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
	
	class Meta:
		user = serializers.ReadOnlyField(source='user.username')
		fields = ['ID', 'user','name', 'origin', 'description', 'cats', 'homes',]
		model = Breed

	"""def to_representation(self, instance):
		data = super(BreedSerializer, self).to_representation(instance)
		data.homes = CatSerializer(instance.cats.home, many=True).data
		return data"""
		

class HumanSerializer(serializers.ModelSerializer):
	"""
	Serializer of the Human Model
	"""
	cats = CatSerializer(read_only=True, many=True)

	def validate_date_of_birth(self, value):
		if value > datetime.datetime.now():
			raise serializers.ValidationError("Date is in the future")
		return value

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	class Meta:
		model = Human
		user = serializers.ReadOnlyField(source='user.username')
		fields = ['ID', 'user', 'name', 'gender', 'date_of_birth', 'description', 'home', 'cats']

class HomeSerializer(serializers.ModelSerializer):
	"""
	Serializer of the Home Model
	"""

	humans = HumanSerializer(read_only = True, many = True)

	def validate_date_of_birth(self, value):
		if value > datetime.datetime.now():
			raise serializers.ValidationError("Date entered is in the future")
		return value

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	class Meta:
		user = serializers.ReadOnlyField(source='user.username')
		model = Home
		fields = ['ID', 'user', 'name', 'address', 'home_type', 'humans']
