from django.db import models
from django import forms
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

class parentQuerySet(models.query.QuerySet):
	def delete(self, *args, **kwargs):
		#print("queryset delete", self)
		for obj in self:
			if obj.enableDelete:
				obj.delete()
			else:
				obj.enabled = False
				obj.save()

class parentManager(models.Manager):
	def get_queryset(self):
		return parentQuerySet(self.model, using=self._db)

class parentModel(models.Model):
	objects = parentManager()
	previous_state = None
	enabled =			models.BooleanField(default=True)
	created =			models.DateTimeField(auto_now_add=True)
	updated =			models.DateTimeField(auto_now=True)
	hasError =			models.BooleanField(default=False)
	errorText =			models.TextField(max_length=9999, default="", blank=True, null=True)
	enableDelete =		models.BooleanField(default=False)
	createdBy =			models.CharField(max_length=256, default = "default")
	host =				models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="%(app_label)s_%(class)s_related")
	# createdFunction =	models.CharField(max_length=256, default = "admin")
	# name =				models.CharField(max_length=256, default = "-empty name-")
	# identifier =		models.CharField(max_length=200, default="----", blank=True, null=True)
	# uniqueCss =			models.TextField(max_length=9999, default="", blank=True, null=True)
	# isProcessed = 		models.BooleanField(default=False)

	# data =				DataField()
	# geometry =			DataField()
	# runFunctions =		DataField(help_text='{"functions": [{"function":"clearDataKeys","variables":{}}]}')
	# uniqueData =		DataField()
	# cssOrder =			[]
	# dataOrder =			[]
	# relativeSave =		[]
	# errorArray =		[]
	# dataToFieldMap =	[]
	# tempData =			{}
	class Meta:
		abstract = True

class geometry(parentModel):
	geometry =			DataField()
	pass