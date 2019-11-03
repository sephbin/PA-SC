from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import json

class profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500, blank=True)
	location = models.CharField(max_length=30, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	def name(self):
		return self.user.first_name +" "+self.user.last_name

class submission(models.Model):
	assignment = models.TextField(max_length=1000)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	link = models.TextField(max_length=1000)
	date = models.DateTimeField(auto_now=False,auto_now_add=True)
	mark = models.TextField(max_length=200,null=True,blank=True)
	def markjson(self):
		try:
			return json.loads(self.mark)
		except:
			return {}

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

class testresult(models.Model):
	test = models.CharField(max_length=256)
	identifier = models.CharField(max_length=256)
	ip = models.CharField(max_length=256)
	pcusername = models.CharField(max_length=256)
	question = models.TextField(max_length=256)
	notes = models.TextField(max_length=1000)
	date = models.DateTimeField(auto_now=True)
	score = models.IntegerField(default=0)

class testquestion(models.Model):
	questionName = models.CharField(max_length=200, unique=True)
	questionText = models.TextField(max_length=1024, null=True, blank=False)
	questionHint = models.TextField(max_length=1024, null=True, blank=False)
	_archjson = models.TextField(max_length=9999)

	def __str__(self):
		return self.questionName
	def archjson(self):
		try:
			return json.loads(self._archjson)
		except:
			return {}