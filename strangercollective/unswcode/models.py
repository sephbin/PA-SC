from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import json
from django import forms
class DataFieldFormField(forms.CharField):

	def prepare_value(self, value):
		try:
			import json
			if value =="{}":
				return value
			else:
				return json.dumps(value)
		except Exception as e:
			return value


class DataField(models.TextField):
	def __init__(self, *args, **kwargs):
		kwargs['max_length'] = 9999
		kwargs['default'] = {}
		kwargs['blank'] = True
		kwargs['null'] = True
		super().__init__(*args, **kwargs)

	def parseString(self, s):
		import json
		try:
			# return "!-%s-!"%(s)
			ns = json.loads(s)
			return ns
		except Exception as e:
			return {}

	def from_db_value(self, value, expression, connection):
		if value is None:
			return {}
		return self.parseString(value)

	def to_python(self, value):
		try:
			py_val = self.parseString(value)
			return py_val
		except Exception as e:
			return {}
	def get_db_prep_save(self, value, connection):
		import json
		try:
			new_value = json.dumps(value)
			return json.dumps(value)
		except Exception as e:
			return json.dumps({"error":str(e)})
	def formfield(self, **kwargs):
		# This is a fairly standard way to set up some defaults
		# while letting the caller override them.
		defaults = {'form_class': DataFieldFormField}
		defaults.update(kwargs)
		return super().formfield(**defaults)


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

class test(models.Model):
	enabled = models.BooleanField()
	testName = models.CharField(max_length=256)
	testPassword = models.CharField(max_length=256)
	timeLimit = models.IntegerField()

class testStart(models.Model):
	identifier = models.CharField(max_length=256)
	test = models.ForeignKey(test, on_delete=models.CASCADE)
	endTime = models.DateTimeField(null=True, blank=True)

	def save(self, *args, **kwargs):
		try:
			if not self.endTime:
				import datetime
				self.endTime = datetime.datetime.now()+datetime.timedelta(hours=self.test.timeLimit)
		except:	pass
		super(testStart, self).save(*args, **kwargs)



class testresult(models.Model):
	test = models.CharField(max_length=256)
	identifier = models.CharField(max_length=256)
	ip = models.CharField(max_length=256)
	pcusername = models.CharField(max_length=256)
	question = models.TextField(max_length=256)
	notes = models.TextField(max_length=1000)
	date = models.DateTimeField(auto_now=True)
	score = models.IntegerField(default=0)
	class Meta:
		ordering = ['test','identifier','question','date']

class testquestion(models.Model):
	questionName		= models.CharField(max_length=200, unique=True)
	questionText		= models.TextField(max_length=1024, null=True, blank=True)
	questionHint		= models.TextField(max_length=1024, null=True, blank=True)
	questionAccuracy	= models.IntegerField(default=1)
	_archjson = models.TextField(max_length=65535, default="{}")

	def __str__(self):
		return self.questionName
	def archjson(self):
		try:
			return json.loads(self._archjson)
		except:
			return {}


class buildingComponent(models.Model):
	name =				models.CharField(max_length=256, default = "-empty name-")
	enabled =			models.BooleanField(default=True)
	created =			models.DateTimeField(auto_now_add=True)
	updated =			models.DateTimeField(auto_now=True)
	hasError =			models.BooleanField(default=False)
	errorText =			models.TextField(max_length=9999, default="", blank=True, null=True)
	enableDelete =		models.BooleanField(default=False)
	createdBy =			models.CharField(max_length=256, default = "default")
	createdFunction =	models.CharField(max_length=256, default = "admin")

	data =				DataField()
	class Meta:
		ordering = ['name']
		unique_together = [['name','createdBy']]
	def delete_start(self):
		pass

	def delete_end(self):
		pass

	def delete(self):
		self.delete_start()
		#print("delete: %s" %(self))
		if self.enableDelete:
			super(buildingComponent, self).delete()
		else:
			self.enabled = False
			self.save()
		self.delete_end()

	def save_start(self):
		#print("default: save_start")
		pass

	def save_end(self):
		#print("default: save_end")
		pass

	def save(self, *args, **kw ):
		self.save_start()
		try:
			upd = self.previous_state["data"]
			#print(upd)
			if upd != self.data:
				upd.update(self.data)
				self.data = upd
		except Exception as e: pass
		super( buildingComponent, self ).save( *args, **kw )
		self.save_end()

