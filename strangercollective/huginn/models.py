from django.db import models

# Create your models here.
class family(models.Model):
	name = models.CharField(max_length = 120)
	gh_script = models.TextField(max_length = 9999, default ="print('no script')")
	def __str__(self):
		return self.name

class functionOb(models.Model):
	functionIdentity	=	models.CharField(max_length=9999)

class parameterOb(models.Model):
	created_at			=	models.DateTimeField(auto_now=True)
	parameterIdentity	=	models.CharField(max_length=255, unique=True)
	parentIdentity		=	models.CharField(max_length=9999)
	parameterVal		=	models.CharField(max_length=9999)
	parameterType		=	models.CharField(max_length=200)
	data_store			=	models.TextField(max_length=200, default="[]", blank=True, null=True)
	sourceParameter		=	models.ManyToManyField('self', through= 'parameterMapThrough', through_fields=('object_to', 'object_from'), symmetrical=False)
	def __str__(self):
		return self.parameterIdentity

class parameterMapThrough(models.Model):
	created_at			= models.DateTimeField(auto_now=True)
	object_from			= models.ForeignKey('parameterOb', on_delete=models.CASCADE, related_name='through_from')
	object_to			= models.ForeignKey('parameterOb', on_delete=models.CASCADE, related_name='through_to')
	# function			= models.ForeignKey('functionOb', on_delete=models.CASCADE, related_name='maps')
	function			= models.CharField(max_length=9999)
	data_store			=	models.TextField(max_length=200, default="[]", blank=True, null=True)

	def __str__(self):
		return self.object_from.parameterIdentity +" -> "+self.object_to.parameterIdentity