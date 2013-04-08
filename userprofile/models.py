from django.db import models
from django.contrib.auth.models import User
from datetime import date

SERVERS = ((1, 'EUNE'), (2, 'EUW'))

class UserProfile(models.Model):
	user = ForeignKey(User,unique=true)
	username = models.CharField('username', max_length=26, 
        help_text='Specify a display name.')
	date_of_birth = models.DateField('Date of birth')
	city = models.CharField('city', max_length=26, Requiered=False)	
	

	def __unicode__(self):
        return self.user.username

class Summoner(models.Model):
	up = ForeignKey(UserProfile)
	name = models.CharField('Summoner name', max_length=26)
	server = models.SmallIntegerField('Server', choices=SERVERS, default=1)

	def __unicode__(self):
        return self.user.name