import factory

from django.contrib.auth.models import User

from cats.models import Home, Cat, Breed, Human

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    id = factory.Faker('pyint')
    username = factory.Faker('name')
    

class HomeFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = factory.Faker('name')
    ID = factory.Faker('pyint')
    address = factory.Faker('text')
    home_type = factory.Iterator(['LD', 'CD'])

    class Meta:
        model = Home
    

class HumanFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    gender = factory.Iterator(['male', 'female', 'others'])
    home = factory.SubFactory(HomeFactory)
    name = factory.Faker('name')
    ID = factory.Faker('pyint')
    date_of_birth = factory.Faker('date_time')
    description = factory.Faker('text')

    class Meta:
        model = Human

class BreedFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = factory.Faker('name')
    ID = factory.Faker('pyint')
    origin = factory.Faker('pystr')
    description = factory.Faker('text')

    class Meta:
        model = Breed
    

class CatFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    owner = factory.SubFactory(HumanFactory)
    breed = factory.SubFactory(BreedFactory)
    name = factory.Faker('name')
    ID = factory.Faker('pyint')
    description = factory.Faker('text')
    gender = factory.Iterator(['male', 'female', 'neutered'])
    date_of_birth = factory.Faker('date_time')
    
    class Meta:
        model = Cat

class HumanWithCats(HumanFactory):
    cats = factory.RelatedFactory(CatFactory, 'owner')

class HomeWithHumans(HomeFactory):
    humans = factory.RelatedFactory(HumanFactory, 'home')

class BreedWithCats(BreedFactory):
    cats = factory.RelatedFactory(CatFactory, 'breed')