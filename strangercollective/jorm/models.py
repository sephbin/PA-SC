from django.db import models


def containsDef(ob, base):
	try:
		base["Contains"].append(ob.object_to.name)
	except:
		base["Contains"] = []
		base["Contains"].append(ob.object_to.name)

def typeDef(ob, base):
	base.update(ob.object_to.data())

def parseThroughs(ob):
	defLU = {"Type": typeDef, "Contains": containsDef, }
	base = {}
	for t in ob.through_from.all():
		defLU[t.function](t, base)
	return base

# Create your models here.
class item_object(models.Model):
	name = models.CharField(max_length = 120)
	json_text = models.TextField(max_length = 9999, default ="{}")
	throughs = models.ManyToManyField('self', through= 'through_object', through_fields=('object_from', 'object_to'), symmetrical=False)
	def __str__(self):
		return self.name
	def data(self):
		import json
		try:
			base = parseThroughs(self)
			obData = json.loads(self.json_text)
			base.update(obData)
			return base
		except Exception as e:
			return str(e)

class through_object(models.Model):
	function_choices = (
	('Contains','Contains'),
	('Type','Type'),
)
	object_from = models.ForeignKey(item_object, on_delete=models.CASCADE, related_name='through_from')
	object_to = models.ForeignKey(item_object, on_delete=models.CASCADE, related_name='through_to')
	json_text = models.TextField(max_length = 9999, default ="{}")
	function = models.CharField(max_length = 256, choices=function_choices)
	def __str__(self):
		return self.object_from.name +" -> "+self.object_to.name