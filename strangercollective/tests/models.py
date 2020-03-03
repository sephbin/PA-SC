from django.db import models
import django.utils.html as dhtml
import json
import uuid
from django import forms
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save, m2m_changed, pre_init, post_init, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.
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

class parentModel(models.Model):
	previous_state = None
	name =			models.CharField(max_length=256, default = "-empty name-")
	enabled =		models.BooleanField(default=True)
	created =		models.DateTimeField(auto_now_add=True)
	updated =		models.DateTimeField(auto_now=True)
	hasError =		models.BooleanField(default=False)
	errorText =		models.TextField(max_length=9999, default="", blank=True, null=True)
	runFunctions =	models.TextField(max_length=9999, default="", blank=True, null=True)
	enableDelete =	models.BooleanField(default=False)

	data = DataField()

	errorArray = []
	class Meta:
		abstract = True
	def __str__(self):
		return str(self.id)+": "+self.name
	# # def data(self):
	# 	try:
	# 		return json.loads(self._data)
	# 	except Exception as e:
	# 		return {"error":str(e)}

	def error(self, message = ""):
		self.hasError = True
		self.errorArray.append("%s"%(message))
	def delDataKeys(self, keys=[]):
		for k in keys:
			try:
				del self.previous_state["data"][k]
			except:	pass
		self.save()
	def delete_start(self):
		pass

	def delete_end(self):
		pass

	def delete(self):
		self.delete_start()
		print("delete: %s" %(self))
		if self.enableDelete:
			super(parentModel, self).delete()
		else:
			self.enabled = False
			self.save()
		self.delete_end()

	def save_start(self):
		print("default: save_start")
		pass

	def save_end(self):
		print("default: save_end")
		pass

	def save( self, *args, **kw ):
		self.errorArray = []
		self.hasError = False
		print("default: save")
		self.save_start()
		try:
			upd = self.previous_state["data"]
			print(upd)
			if upd != self.data:
				upd.update(self.data)
				self.data = upd
		except Exception as e: pass
		self.runFunctions = ""
		self.errorText = "\n".join(self.errorArray)
		super( parentModel, self ).save( *args, **kw )
		self.save_end()
	
	@staticmethod

	# @receiver(post_init, self)
	def remember_state(sender, **kwargs):
		# print("remember_state internal")
		# print(sender)
		try:
			instance = kwargs.get('instance')
			remember = {
				"data": instance.data,
			}
			instance.previous_state = remember
		except: pass

class tokenmap(parentModel):
	directParent = "-"
class token(parentModel):
	position =		DataField()
	tokenmap = models.ForeignKey(tokenmap, on_delete=models.CASCADE, related_name="tokens", blank=True, null=True)
	directParent = "tokenmap"
	class Meta:
		ordering = ['name']

def pokeParent(sender, **kwargs):
		try:
			instance = kwargs.get('instance')
			try:
				getattr(instance, instance.directParent).save()
			except:
				for po in getattr(instance, instance.directParent).all():
					# print("po",po)
					po.save()
		except: pass

for subclass in parentModel.__subclasses__():
	post_init.connect(subclass.remember_state, sender=subclass)
	post_save.connect(pokeParent, sender=subclass)
	post_delete.connect(pokeParent, sender=subclass)