from django.db import models

from django.db.models.signals import post_save, post_init, post_delete
# Create your models here.
class family(models.Model):
	name = models.CharField(max_length = 120)
	gh_script = models.TextField(max_length = 9999, default ="print('no script')")
	def __str__(self):
		return self.name

class functionOb(models.Model):
	functionIdentity	=	models.CharField(max_length=255)

class parameterObject(models.Model):
	param_created_at			=	models.DateTimeField(auto_now=True)
	parameterIdentity	=	models.CharField(max_length=255, unique=True)
	parentIdentity		=	models.CharField(max_length=255)
	parameterVal		=	models.CharField(max_length=65535)
	parameterType		=	models.CharField(max_length=200)
	data_text			=	models.TextField(max_length=65535, default="[]", blank=True, null=True)
	sourceParameter		=	models.ManyToManyField('self', through= 'parameterMapThroughObject', through_fields=('object_to', 'object_from'), symmetrical=False)
	def __str__(self):
		return self.parameterIdentity

class parameterMapThroughObject(models.Model):
	map_created_at			= models.DateTimeField(auto_now=True)
	object_from			= models.ForeignKey('parameterObject', on_delete=models.CASCADE, related_name='through_from')
	object_to			= models.ForeignKey('parameterObject', on_delete=models.CASCADE, related_name='through_to')
	# function			= models.ForeignKey('functionOb', on_delete=models.CASCADE, related_name='maps')
	function			= models.CharField(max_length=255)
	data_text			=	models.TextField(max_length=200, default="[]", blank=True, null=True)

	def __str__(self):
		return self.object_from.parameterIdentity +" -> "+self.object_to.parameterIdentity



class DataField(models.TextField):
	# def __init__(self, *args, **kwargs):
 #        # kwargs['primary_key'] = True
 #        super().__init__(*args, **kwargs)

	def parseString(self, s):
		import json
		try:
			# return "!-%s-!"%(s)
			return json.loads(s)
		except Exception as e:
			return str(e)

	def from_db_value(self, value, expression, connection):
		if value is None:
			return {}
		return self.parseString(value)

	def to_python(self, value):
		return self.parseString(value)
	def get_db_prep_save(self, value, connection):
		import json
		try:
			return json.dumps(value)
		except Exception as e:
			print(e)
			return json.dumps({"error":str(e)})
	

class testModel(models.Model):
	
	previous_state = None
	data = DataField(max_length=255, default="{}", blank=True, null=True)
	# data.printStuff()
	@property
	def foo(self):
		return "Hello"
	
	def delDataKeys(self, keys=[]):
		for k in keys:
			try:
				del self.previous_state["data"][k]
			except:	pass
		self.save()

	@staticmethod
	def remember_state(sender, **kwargs):
		instance = kwargs.get('instance')
		remember = {
			"data": instance.data,
		}
		instance.previous_state = remember


	def save(self, *args, **kwargs):
		try:
			upd = self.previous_state["data"]
			if upd != self.data:
				upd.update(self.data)
				self.data = upd
		except Exception as e: pass
		super(testModel, self).save(*args, **kwargs)
post_init.connect(testModel.remember_state, sender=testModel)