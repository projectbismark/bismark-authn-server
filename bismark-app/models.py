from django.db import models
from django.contrib.auth.models import User
from django_countries import CountryField

#Router object stores user information
class Router(models.Model):
	def __unicode__(self): 
		 return self.user.email
	user = models.ForeignKey(User)
	isp = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	country = CountryField()
	service_type = models.CharField(max_length=100)
	service_plan = models.CharField(max_length=100)
	drate = models.CharField(max_length=100, blank=True)
	urate = models.CharField(max_length=100, blank=True)
	node_id = models.CharField(max_length=100)
