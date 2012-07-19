from django.db import models
from django.contrib.auth.models import User

class Router(models.Model):
	def __unicode__(self): 
		 return self.user.email
	user = models.ForeignKey(User)
	isp = models.CharField(max_length=100)
	location = models.CharField(max_length=100)
	service_type = models.CharField(max_length=100)
	service_plan = models.CharField(max_length=100)
	drate = models.CharField(max_length=100)
	urate = models.CharField(max_length=100)
