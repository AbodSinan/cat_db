import factory

from django.contrib.auth.models import User

from cats.models import Home, Cat, Breed, Human


class HomeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Home

class HumanFactory(factory.django.DjangoModelFactory):
    home = factory.SubFactory(HomeFactory)
    class Meta:
        model = Home
    

class BreedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Breed
    

class CatFactory(factory.django.DjangoModelFactory):
    owner = factory.SubFactory(HumanFactory)
    breed = factory.SubFactory(HomeFactory)
    class Meta:
        model = User

class HumanWithCats(HumanFactory):
    cats = factory.RelatedFactory(CatFactory, 'owner')

class HomeWithHumans(HomeFactory):
    humans = factory.RelatedFactory(HumanFactory, 'home')

class BreedWithCats(BreedFactory):
    cats = factory.RelatedFactory(CatFactory, 'breed')