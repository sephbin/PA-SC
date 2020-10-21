from django.db import models
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.safestring import mark_safe
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.db.models.signals import post_save, post_init, pre_save
from django.dispatch import receiver
from django import forms


def coolUpdate(original, new):
	appendList = ["class"]
	originaldict = dict(original)
	newdict = dict(new)
	for k,v in originaldict.items():
		if type(v) == type({}):
			try:
				newdict[k] = coolUpdate(v, newdict[k])
			except:
				pass
		if k in appendList:
			try:	newdict[k] = newdict[k]+" "+v
			except:	pass
			try:	newdict[k] = " ".join(list(filter(None,sorted(set((newdict[k].split(" ")))))))
			except:	pass
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
		kwargs['max_length'] = 99999
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

class parentModel(models.Model):
	# objects =			parentManager()
	previous_state =	None
	name =				models.CharField(max_length=256, default = "-empty name-")
	enabled =			models.BooleanField(default=True)
	created =			models.DateTimeField(auto_now_add=True)
	updated =			models.DateTimeField(auto_now=True)
	hasError =			models.BooleanField(default=False)
	errorText =			models.TextField(max_length=9999, default="", blank=True, null=True)
	enableDelete =		models.BooleanField(default=False)
	createdBy =			models.CharField(max_length=256, default = "default")
	createdFunction =	models.CharField(max_length=256, default = "admin")
	uniqueCss =			models.TextField(max_length=9999, default="", blank=True, null=True)

	data =				DataField()
	runFunctions =		DataField()
	uniqueData =		DataField()
	cssOrder =			[]
	dataOrder =			[]
	relativeSave =		[]
	errorArray =		[]
	dataToFieldMap =	[]
	tempData =			{}

	@property
	def css( self):
		out_css = ""
		for step in self.cssOrder:
			try:	out_css += getattr(self,step).uniqueCss+"\n"
			except:	pass
		out_css += self.uniqueCss
		return out_css
	class Meta:
		abstract = True
	def __str__(self):
		return str(self.id)+": "+self.name
	def saveRelative(self):
		print("saveRelative")
		print(self.relativeSave)
		for i in self.relativeSave:
			try:
				background_saveRelative(self.__class__.__name__, self.id, self.relativeSave)
			except Exception as e:
				print(e)
	def error(self, message = ""):
		self.hasError = True
		self.errorArray.append("%s"%(message))
	def delDataKeys(self, keys=[]):
		#print("delDataKeys")
		for k in keys:
			try:
				del self.previous_state["data"][k]
				#print(self.previous_state["data"])
			except:	pass
		self.uniqueData = self.previous_state["data"]
	def clearDataKeys(self, variables):
		print("CLEARDATAKEYS")
		self.previous_state["data"] = {}
	@property
	def clearCss(self):
		pass
	@property
	def set_data(self):
		print(self,"set_data")
		special = ["css", "itemsInheritance",]
		d = {"class":""}
		try:
			for step in self.dataOrder:
				print("step",step)
				if step not in special:
					try:
						newdata = dict(getattr(self,step).data)
						print(newdata)
						d = coolUpdate(d, newdata)
					except:	pass
				elif step == "itemsInheritance":
					items = self.muninn_dev_item_related.filter(enabled=True)
					print(">>>>>>>>>", items)
					for i in items:
						try:
							newdata = dict(i.data["containerInherit"])
							d = coolUpdate(d, newdata)
						except:	pass
				elif step == "css":
					self.clearCss
					d = apply_css(self, self.css)
				self.tempData = d
			newdata = dict(self.uniqueData)
			d = coolUpdate(d, newdata)
			self.tempData = d
			print(d)
			return d
		except Exception as e:
			return {"error":str(e)}
	
	def runAllFunctions(self, application=None):
		print("runAllFunctions")
		try:
			print(self.runFunctions)
			for f in self.runFunctions["functions"]:
				try:
					print(f)
					getattr(self,f["function"])(f["variables"])
				except: pass
		except Exception as e:	return {"error": str(e)}

	def dataToFields(self):
		fields = self.dataToFieldMap
		for f in fields:
			try:
				val = self.data[f]
				setattr(self, f, val)
			except: pass
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
		#print("default: save_start")
		pass

	def save_end(self):
		#print("default: save_end")
		pass

	def save(self, *args, **kw ):
		self.errorArray = []
		self.hasError = False
		#print("default: save")
		self.save_start()
		self.runAllFunctions()
		self.data = self.set_data
		try:
			upd = self.previous_state["data"]
			#print(upd)
			if upd != self.uniqueData:
				upd.update(self.uniqueData)
				self.uniqueData = upd
		except Exception as e: pass
		self.runFunctions = {"functions":[
			# {"function":"delDataKeys","variables":["error","class","containerInherit"]}
			]}
		self.dataToFields()
		self.errorText = "\n".join(self.errorArray)
		super( parentModel, self ).save( *args, **kw )
		self.saveRelative()
		self.save_end()




	@staticmethod

	# @receiver(post_init, self)
	def remember_state(sender, **kwargs):
		#print("remember_state internal")
		#print(sender)
		try:
			instance = kwargs.get('instance')
			remember = {
				"data": instance.uniqueData,
			}
			instance.previous_state = remember
		except: pass

class obClass(parentModel):
	pass

class feature(parentModel):
	obClass =	models.ForeignKey('obClass', on_delete=models.SET_NULL, null=True, blank=True, related_name="%(app_label)s_%(class)s_related")


class characterTemplate(parentModel):
	stOffset =		models.IntegerField(default=0)
	dxOffset =		models.IntegerField(default=0)
	iqOffset =		models.IntegerField(default=0)
	htOffset =		models.IntegerField(default=0)
	hpOffset =		models.IntegerField(default=0)
	willOffset =	models.IntegerField(default=0)
	perOffset =		models.IntegerField(default=0)
	fpOffset =		models.IntegerField(default=0)
	smOffset =		models.IntegerField(default=0)
	bsOffset =		models.FloatField(default=0)
	bmOffset =		models.IntegerField(default=0)

	features =		models.ManyToManyField('feature', through='feature_relative', through_fields=('characterTemplate', 'feature'), blank=True,)
	choices =		models.ManyToManyField('choice', blank=True,)

class choice(parentModel):
	characterTemplate =	models.ForeignKey("characterTemplate", on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related")
	choiceType =		models.CharField(max_length=256, default = "oneOfPackage")
	packageChoices =	models.ManyToManyField('characterTemplate', blank=True)
	featuresChoices =	models.ManyToManyField('feature', through='feature_relative', through_fields=('choice', 'feature'), blank=True,)


class feature_relative(parentModel):
	characterTemplate =	models.ForeignKey("characterTemplate", on_delete=models.CASCADE, null=True, blank=True, related_name='rel_skill_template')
	choice =	models.ForeignKey("choice", on_delete=models.CASCADE, null=True, blank=True, related_name='rel_skill_template')
	obClass =	models.ForeignKey('obClass', on_delete=models.SET_NULL, null=True, blank=True, related_name="%(app_label)s_%(class)s_related")
	feature =			models.ForeignKey(feature, on_delete=models.CASCADE, related_name='rel_skill_template')
	rank =				models.IntegerField(null=True, blank=True,)
	class Meta:
		ordering = ['feature']
	
	def save_start(self):
		self.obClass = self.feature.obClass
	def cost(self):
		if self.rank:
			if self.rank <= 2:
				return self.rank
			else:
				return (self.rank-2)*4
	# def skill_challenge(self):
	# 	return self.skill.skill_challenge
	# def skill_attribute(self):
	# 	return self.skill.skill_attribute
	# def relative_skill(self):
	# 	val = 0
	# 	if self.rank:
	# 		  val = self.rank
	# 	lookup = {"E":-1,"A":-2,"H":-3,"VH":-4}
	# 	rel = val+lookup[self.skill.skill_challenge]
	# 	atr = self.skill.skill_attribute
	# 	operator = ""
	# 	if rel > 0:
	# 		operator = "+"
	# 	if rel != 0:
	# 		return atr.upper()+operator+str(rel)
	# 	else:
	# 		return atr.upper()

def charXmlPath(instance, filename):
	from django.conf import settings
	import os
	import datetime
	return os.path.join("crowbar","characters", instance.name+"-"+str(instance.id), datetime.datetime.now().strftime("%Y%m%d-%H%M"), filename)
class character(parentModel):
	gcaData = DataField()

	gcaXml = models.FileField(upload_to=charXmlPath, blank=True, null=True)
	def save_start(self):
		import json
		import xmltodict
		with open("D:\\Users\\s-abutler\\Downloads\\GURPS\\GURPS 4e\\GURPS 4e Character Assistant\\Chars\\Sten\\Sten (Owen).gca4.XML") as xml_file:
			dd = xmltodict.parse(xml_file.read())
			self.gcaData = {
				"Traits":dd['Character']["Traits"],
				"General":dd['Character']["General"],
			}
		pass

for subclass in parentModel.__subclasses__():
	post_init.connect(subclass.remember_state, sender=subclass)