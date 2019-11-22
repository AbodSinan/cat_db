import factory

from django.contrib.auth.models import User

from cats.models import Home, Cat, Breed, Human

class UserFactory(factory.django.DjangoModelFactory):
    """
    A factory to generate User Instances
    """
    class Meta:
        model = User
    id = factory.Faker('pyint')
    username = factory.Faker('name')
    

class HomeFactory(factory.django.DjangoModelFactory):
    """
    A factory to generate Home instances
    """
    user = factory.SubFactory(UserFactory)
    name = factory.Faker('name')
    ID = factory.Faker('pyint')
    address = factory.Faker('text')
    home_type = factory.Iterator(['LD', 'CD'])

    class Meta:
        model = Home
    

class HumanFactory(factory.django.DjangoModelFactory):
    """
    A factory to generate Human instances
    """
    user = factory.SubFactory(UserFactory)
    gender = factory.Iterator(['male', 'female', 'others'])
    home = factory.SubFactory(HomeFactory)
    name = factory.Faker('name')
    ID = factory.Faker('pyint')
    date_of_birth = factory.Faker('date')
    description = factory.Faker('text')

    class Meta:
        model = Human

class BreedFactory(factory.django.DjangoModelFactory):
    """
    A factory to generate Breed instances
    """
    user = factory.SubFactory(UserFactory)
    name = factory.Faker('name')
    ID = factory.Faker('pyint')
    origin = factory.Faker('pystr')
    description = factory.Faker('text')

    class Meta:
        model = Breed
    

class CatFactory(factory.django.DjangoModelFactory):
    """
    A factory to generate Cat instances
    """
    user = factory.SubFactory(UserFactory)
    owner = factory.SubFactory(HumanFactory)
    breed = factory.SubFactory(BreedFactory)
    name = factory.Faker('name')
    ID = factory.Faker('pyint')
    description = factory.Faker('text')
    gender = factory.Iterator(['male', 'female', 'neutered'])
    date_of_birth = factory.Faker('date')
    
    class Meta:
        model = Cat

class HumanWithCats(HumanFactory):
    """
    a modified version of HumanFactory to generate a related Cat instance
    """
    cats = factory.RelatedFactory(CatFactory, 'owner')

class HomeWithHumans(HomeFactory):
    """
    a modified version of HomeFactory with related Human instances
    """
    humans = factory.RelatedFactory(HumanFactory, 'home')

class BreedWithCats(BreedFactory):
    """
    a modified version of BreedFactory with related Cats
    """
    cats = factory.RelatedFactory(CatFactory, 'breed')