from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class TimeStampedModel(models.Model):
	"""
	A simple base model that will contain date created and modified
	will be used on other classes
	"""

	ID = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 50)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	class Meta:
		abstract = True

class Cat(TimeStampedModel):
	"""
	The model that contains the cat's information
	"""

	gender = models.CharField(max_length = 10)
	date_of_birth = models.DateTimeField()
	description = models.TextField()
	breed = models.ForeignKey('Breed', on_delete= models.CASCADE, related_name='cats')
	owner = models.ForeignKey('Human', on_delete= models.CASCADE, related_name='cats')
	user = models.ForeignKey('auth.User', related_name='cats', on_delete=models.CASCADE)

class Breed(TimeStampedModel):
	"""
	The model that contains the information about the breed of the cat
	"""

	user = models.ForeignKey('auth.User', related_name='breeds', on_delete=models.CASCADE)
	origin = models.CharField(max_length = 50)
	description = models.TextField()
	
	def __str__(self):
		return self.name

class Human(TimeStampedModel):
	"""
	Model the contains human's information
	"""

	user = models.ForeignKey('auth.User', related_name='humans', on_delete=models.CASCADE)
	gender = models.CharField(max_length = 10)
	date_of_birth = models.DateTimeField()
	description = models.TextField()
	home = models.ForeignKey('Home', on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class Home(TimeStampedModel):
	"""
	Model that contains Home information
	"""

	HOME_CHOICES = [
		('LD', 'Landed'),
		('CD', 'Condominium')
	]
	user = models.ForeignKey('auth.User', related_name='homes', on_delete=models.CASCADE)
	home_type = models.CharField(max_length = 20, choices=HOME_CHOICES)
	address = models.TextField()

	def __str__(self):
		return self.name





