from django.db import models
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.safestring import mark_safe
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.db.models.signals import post_save
from django.dispatch import receiver

from background_task import background

from PIL import Image
import math
from io import BytesIO
import sys, os
import math
import json
import requests
# from django.contrib.auth.models import User
# from taggit.managers import TaggableManager
# Create your models here.
package = str(__package__)

@background(schedule=1)
def splitImage(ob_id):
	print("SPLIT IMAGE")
	log=[]
	#Opening the uploaded image
	delim = "/"
	if os.name == 'nt':
		delim = "\\"
	# print("delim",delim)
	ob = get_object_or_404(map, id=ob_id)
	im = Image.open(ob.image)
	w, h = im.size
	# print("wh:",w,h)


	fullRes = w
	if h > w: fullRes = h
	maxdiv = math.ceil(fullRes/256)
	# print("maxdiv:",maxdiv)
	maxzoom = 0
	dyndiv = 1
	while dyndiv*2 < maxdiv:
		dyndiv = 2 ** maxzoom
		maxzoom += 1
	extra = 0
	maxzoom += extra
	# print("maxzoom:",maxzoom)
	zooms = list(range(maxzoom+1))
	basepath = settings.MEDIA_ROOT+"maps"
	# basepath = basepath.replace("/","")
	mapPath = basepath+"\\%s"%(ob.id)
	# print("mappath",mapPath)
	try:                    os.makedirs(mapPath.replace("\\",delim))
	except Exception as e:  log.append(str(e))
	for z in zooms:
		print("zooms: ",z)
		revzooms = zooms[::-1]
		scale = revzooms[zooms.index(z)]
		scale += -1*extra
		# print("Scale",scale)
		zpath = mapPath+"\\%s"%(str(z))
		zpath = zpath.replace("\\",delim)
		try:                    os.mkdir(zpath)
		except Exception as e:  log.append(str(e))
		ylist = list(range(2**z))
		# print(ylist)
		for y in ylist:
			tilepath = zpath+"\\%s"%(str(y))
			try:                    os.mkdir(tilepath.replace("\\",delim))
			except Exception as e:  log.append(str(e))
			xlist = list(range(2**z))
			for x in xlist:
				zscale = 2**scale
				# print("zscale", zscale)
				nw = math.ceil(w/zscale)
				nh = math.ceil(h/zscale)
				x0, x1 = (x*265)+x, ((x+1)*265)+x
				y0, y1 = (y*265)+y, ((y+1)*265)+y
				if x0 <= nw and y0 <= nh:
					scaled_image =  im.resize((nw,nh), Image.ANTIALIAS)
					path = tilepath+"\\%s.png" %(str(x))
					temp = scaled_image.crop((x0, y0, x1, y1)) #x0 y0 x1 y1
					temp.save(path.replace("\\",delim), format='PNG', quality=100)
	return log

class campaign(models.Model):
	name = models.CharField(max_length = 120)
	gameMaster = models.ManyToManyField(User, related_name=package+"_gamemaster", blank=True)
	player = models.ManyToManyField(User, related_name=package+"_player", blank=True)
	def __str__(self):
		return self.name
class characterType(models.Model):
	type = models.CharField(max_length = 120)
	def __str__(self):
		return self.type
class race(models.Model):
	race = models.CharField(max_length = 120)
	def __str__(self):
		return self.race
class status(models.Model):
	status = models.CharField(max_length = 120)
	def __str__(self):
		return self.status

class specialmodifier(models.Model):
	name = models.CharField(max_length = 120)
	description = models.TextField(max_length = 9999)
	modifier = models.IntegerField()
	def __str__(self):
		return self.name


class advantage(models.Model):
	campaign = models.ManyToManyField(campaign, related_name="advantage")
	name = models.CharField(max_length = 120)
	url = models.CharField(max_length = 999, null=True, blank=True)
	basecost = models.IntegerField()
	advchoices = (
		('P', 'Physical'),
		('M', 'Mental'),
		('B', 'Physical/Mental'),
	)
	advsources = (
		('E', 'Exotic'),
	)
	type = models.CharField(
		max_length=1,
		choices=advchoices,
		null=True,
		blank=True,
	)
	sources = models.CharField(
		max_length=1,
		choices=advsources,
		null=True,
		blank=True,
	)
	description = models.TextField(max_length = 9999)
	speciallimitations = models.ForeignKey(specialmodifier, on_delete=models.CASCADE, null=True, blank=True)
	effect = models.TextField(max_length = 9999, null=True, blank=True)
	# specifier = models.CharField(max_length = 120, blank=True, null=True,)
	def __str__(self):
		return self.name

class disadvantage(models.Model):
	campaign = models.ManyToManyField(campaign, related_name="disadvantage")
	name = models.CharField(max_length = 120)
	url = models.CharField(max_length = 999, null=True, blank=True)
	basecost = models.IntegerField()
	disadvchoices = (
		('P', 'Physical'),
		('M', 'Mental'),
		('B', 'Physical/Mental'),
	)
	disadvsources = (
		('E', 'Exotic'),
	)
	type = models.CharField(
		max_length=1,
		choices=disadvchoices,
		null=True,
		blank=True,
	)
	sources = models.CharField(
		max_length=1,
		choices=disadvsources,
		null=True,
		blank=True,
	)
	description = models.TextField(max_length = 9999)
	speciallimitations = models.ForeignKey(specialmodifier, on_delete=models.CASCADE, null=True, blank=True)
	# specifier = models.CharField(max_length = 120, blank=True, null=True,)
	def __str__(self):
		return self.name

class skill(models.Model):
	campaign = models.ManyToManyField(campaign, related_name="skill")
	skill_name = models.CharField(max_length=120)
	url = models.CharField(max_length = 999, null=True, blank=True)
	skillchchoices = (
		('E', 'Easy'),
		('A', 'Average'),
		('H', 'Hard'),
		('VH', 'Very Hard'),
	)
	skillatchoices = (
		('dx', 'Dexterity'),
		('iq', 'Intelligence'),
		('ht', 'Health'),
		('per', 'Perception'),
		('will', 'Will'),
	)
	skill_challenge = models.CharField(max_length=2, choices=skillchchoices, null=True, blank=True)
	skill_attribute = models.CharField(max_length=4, choices=skillatchoices, null=True, blank=True)
	skill_description = models.TextField(max_length = 9999, blank=True, null=True)
	skill_defaults = models.TextField(max_length = 9999, blank=True, null=True)
	class Meta:
		ordering = ['skill_name']
	def __str__(self):
		return self.skill_name

class possession_category(models.Model):
	possession_category_name = models.CharField(max_length=256)
	def __str__(self):
		return self.possession_category_name

class possession(models.Model):
	campaign = models.ManyToManyField(campaign, related_name="possession")
	possession_name = models.CharField(max_length=120)
	possession_description = models.TextField(max_length = 9999, blank=True, null=True)
	possession_weight = models.IntegerField(default=0)
	possession_cost = models.IntegerField(default=0)
	possession_category = models.ManyToManyField(possession_category, related_name="possession")
	####WEAPONS ARMOURS ETC ####
	meleeStatsText = models.TextField(max_length = 9999, blank=True, null=True)
	rangeStatsText = models.TextField(max_length = 9999, blank=True, null=True)
	armourStatsText = models.TextField(max_length = 9999, blank=True, null=True)
	class Meta:
		ordering = ['possession_name']
	def __str__(self):
		return self.possession_name
	def meleeStats(self):
		try:
			return json.loads(self.meleeStatsText)
		except:
			return []
	def rangeStats(self):
		try:
			return json.loads(self.rangeStatsText)
		except:
			return []
class language(models.Model):
	language_name = models.CharField(max_length=120)
	def __str__(self):
		return self.language_name

class character(models.Model):
	campaign = models.ForeignKey(campaign, on_delete=models.CASCADE, related_name="character")
	characterType = models.ForeignKey(characterType, on_delete=models.CASCADE)
	firstname = models.CharField(max_length = 120)
	lastname = models.CharField(max_length = 120)
	race = models.ForeignKey(race, on_delete=models.CASCADE)
	occupation = models.CharField(max_length = 120)
	status = models.ForeignKey(status, on_delete=models.CASCADE)
	attributesText =  models.CharField(max_length = 2000)
	drText =  models.CharField(max_length = 2000)
	advantages = models.ManyToManyField(advantage, through='rel_advantage',through_fields=('character', 'advantage'), blank=True)
	disadvantages = models.ManyToManyField(disadvantage, through='rel_disadvantage',through_fields=('character', 'disadvantage'), blank=True,)
	skills = models.ManyToManyField(skill, through='rel_skill',through_fields=('character', 'skill'), blank=True,)
	# techniques = models.ForeignKey(skill, on_delete=models.CASCADE)
	# spells = models.ForeignKey(spell, on_delete=models.CASCADE)
	languages = models.ManyToManyField(language, through='rel_language',through_fields=('character', 'language'), blank=True,)
	# languages = models.ForeignKey(language, on_delete=models.CASCADE)
	# cultures = models.ForeignKey(culture, on_delete=models.CASCADE)
	reactions = models.CharField(max_length = 2000)
	# possessions = models.ForeignKey(possession, on_delete=models.CASCADE)
	possessions = models.ManyToManyField(possession, through='rel_possession',through_fields=('character', 'possession'), blank=True,)
	connection = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,)
	notes =  models.CharField(max_length = 9000, null=True, blank=True,)
	##############
	##ATTRIBUTES##
	##############
	st = models.IntegerField(default=10)
	dx = models.IntegerField(default=10)
	iq = models.IntegerField(default=10)
	ht = models.IntegerField(default=10)
	hp = models.IntegerField(default=10)
	will = models.IntegerField(default=10)
	per = models.IntegerField(default=10)
	fp = models.IntegerField(default=10)
	sm = models.IntegerField(default=1)
	bs = models.FloatField(default=5)
	bm = models.IntegerField(default=5)


	def __str__(self):
		return self.firstname+" "+self.lastname
	def displayname(self):
		return self.firstname+" "+self.lastname
	def damage(self):
		lookup = {"1":{"Thrust":{"die":1,"mod":-6},"Swing":{"die":1,"mod":-5}},"2":{"Thrust":{"die":1,"mod":-6},"Swing":{"die":1,"mod":-5}},"3":{"Thrust":{"die":1,"mod":-5},"Swing":{"die":1,"mod":-4}},"4":{"Thrust":{"die":1,"mod":-5},"Swing":{"die":1,"mod":-4}},"5":{"Thrust":{"die":1,"mod":-4},"Swing":{"die":1,"mod":-3}},"6":{"Thrust":{"die":1,"mod":-4},"Swing":{"die":1,"mod":-3}},"7":{"Thrust":{"die":1,"mod":-3},"Swing":{"die":1,"mod":-2}},"8":{"Thrust":{"die":1,"mod":-3},"Swing":{"die":1,"mod":-2}},"9":{"Thrust":{"die":1,"mod":-2},"Swing":{"die":1,"mod":-1}},"10":{"Thrust":{"die":1,"mod":-2},"Swing":{"die":1,"mod":0}},"11":{"Thrust":{"die":1,"mod":-1},"Swing":{"die":1,"mod":1}},"12":{"Thrust":{"die":1,"mod":-1},"Swing":{"die":1,"mod":2}},"13":{"Thrust":{"die":1,"mod":0},"Swing":{"die":2,"mod":-1}},"14":{"Thrust":{"die":1,"mod":0},"Swing":{"die":2,"mod":0}},"15":{"Thrust":{"die":1,"mod":1},"Swing":{"die":2,"mod":1}},"16":{"Thrust":{"die":1,"mod":1},"Swing":{"die":2,"mod":2}},"17":{"Thrust":{"die":1,"mod":2},"Swing":{"die":3,"mod":-1}},"18":{"Thrust":{"die":1,"mod":2},"Swing":{"die":3,"mod":0}},"19":{"Thrust":{"die":2,"mod":-1},"Swing":{"die":3,"mod":1}},"20":{"Thrust":{"die":2,"mod":-1},"Swing":{"die":3,"mod":2}}}
		damkey = str(self.st)
		return(lookup[damkey])
	def otherSkills(self):
		allSkills = self.campaign.skill.all()
		allCharSkills = self.relskill.all()
		allSkills = list(map(lambda x: x, allSkills))
		allCharSkills = list(map(lambda x: x.skill, allCharSkills))
		for cs in allCharSkills:
			try:    allSkills.remove(cs)
			except: pass
		return(allSkills)
	def possessionTotals(self):
		cost = 0
		weight = 0
		for p in self.relpossession.all():
			cost += p.cost()
			weight += p.weight()
		return {'cost':cost, 'weight': weight}

	def cost(self):
		tally = 0
		attr = {
		"stCost":(self.st-10)*10,
		"dxCost":(self.dx-10)*20,
		"iqCost":(self.iq-10)*20,
		"htCost":(self.ht-10)*10,
		"hpCost":(self.hp-self.st)*2,
		"willCost":(self.will-self.iq)*5,
		"perCost":(self.per-self.iq)*5,
		"fpCost":(self.fp-self.ht)*3,
		"bsCost":int(((self.bs*4)-(self.ht+self.dx))*5),
		"bmCost":((self.bm)-math.floor((self.ht+self.dx)/4))*5,
		}
		for a in attr:
			tally += int(attr[a])
		listables = [self.reladvantage.all(),self.reldisadvantage.all(),self.relskill.all(),self.rellanguage.all()]
		for l in listables:
			for t in l:
				try:
					tally += t.cost()
				except:
					pass
		costs = {
		"total": tally,
		"attributes": attr,
		}
		return costs
	def save(self, *args, **kwargs):
		super(character, self).save(*args, **kwargs)
		payload = {'value1': self.firstname+" "+self.lastname+" ["+str(self.cost()["total"])+"]", 'value2': 'http://www.strangercollective.com/rpg/'+str(self.id)}
		try:
			r = requests.post("https://maker.ifttt.com/trigger/crowbarcharacteredit/with/key/bhFn8UCEstaDR_dRNGLoBd", data=payload)
		except:
			pass


class modPackage(models.Model):
	# relAdv = models.ForeignKey(rel_advantage, on_delete=models.CASCADE)
	# packageName = models.CharField(max_length = 120)
	modifiers = models.ManyToManyField("modifier", blank=True,)
	def __str__(self):
		mods = self.modifier_set.all()
		txt = []
		for i in mods:
			txt.append(str(i))
		txt = "; ".join(txt)
		return txt

class modifier(models.Model):
	# modPackage = models.ForeignKey(modPackage, on_delete=models.CASCADE)
	name = models.CharField(max_length = 120)
	description = models.CharField(max_length = 120)
	modifier = models.IntegerField()
	def __str__(self):
		return self.name

class rel_advantage(models.Model):
	character = models.ForeignKey(character, on_delete=models.CASCADE, related_name='reladvantage')
	advantage = models.ForeignKey(advantage, on_delete=models.CASCADE, related_name='reladvantage')
	modifiers = models.ForeignKey(modPackage, on_delete=models.CASCADE, null=True, blank=True,)
	# modifiers = models.ManyToManyField(modifier, blank=True,)
	rank = models.IntegerField(null=True, blank=True,)
	# def mods(self):
		# return self.modifiers
	def cost(self):
		cost = self.advantage.basecost
		if self.rank:
			cost = cost*self.rank
		modCf = 100
		try:
			mods = self.modifiers.modifier_set.all()
			for i in mods:
				modCf += i.modifier
		except:
			pass
		if modCf < 20:
			modCf = 20
		modval = modCf/100
		
		moddedcost = int(math.ceil(float(cost)*float(modval)))
		return moddedcost
	def effect(self):
		if self.advantage.effect:
			ef = json.loads(self.advantage.effect)
			return ef
		else:
			return []
	def name(self):
		try:
			modStr = []
			for i in self.modifiers.modifier_set.all():
				modStr.append("%s, %s%%"%(i.name, i.modifier))
			modStr = "; ".join(modStr)
			return str(self.advantage)+" ("+modStr+")"
		except:
			return str(self.advantage)
	def __str__(self):
		return str(self.rank)

class rel_disadvantage(models.Model):
	character =     models.ForeignKey(character, on_delete=models.CASCADE, related_name='reldisadvantage')
	disadvantage =  models.ForeignKey(disadvantage, on_delete=models.CASCADE, related_name='reldisadvantage')
	# modifiers = models.ForeignKey(modPackage, on_delete=models.CASCADE,null=True,blank=True,)
	# modifiers = models.ManyToManyField(modifier, blank=True,)
	rank = models.IntegerField(null=True, blank=True,)
	# def mods(self):
		# return self.modifiers
	def cost(self):
		cost = self.disadvantage.basecost
		if self.rank:
			cost = cost*self.rank
		modCf = 100
		try:
			mods = self.modifiers.modifier_set.all()
			for i in mods:
				modCf += i.modifier
		except:
			pass
		modval = modCf/100
		
		moddedcost = int(math.ceil(float(cost)*float(modval)))
		return moddedcost
	def name(self):
		try:
			modStr = []
			for i in self.modifiers.modifier_set.all():
				modStr.append("%s, %s%%"%(i.name, i.modifier))
			modStr = "; ".join(modStr)
			return str(self.disadvantage)+" ("+modStr+")"
		except:
			return str(self.disadvantage)
	def __str__(self):
		return str(self.rank)

class rel_skill(models.Model):
	character =     models.ForeignKey(character, on_delete=models.CASCADE, related_name='relskill')
	skill =  models.ForeignKey(skill, on_delete=models.CASCADE, related_name='relskill')
	rank = models.IntegerField(null=True, blank=True,)
	class Meta:
		ordering = ['skill']
	def cost(self):
		if self.rank:
			if self.rank <= 2:
				return self.rank
			else:
				return (self.rank-2)*4
	def skill_challenge(self):
		return self.skill.skill_challenge
	def skill_attribute(self):
		return self.skill.skill_attribute
	def relative_skill(self):
		val = 0
		if self.rank:
			  val = self.rank
		lookup = {"E":-1,"A":-2,"H":-3,"VH":-4}
		rel = val+lookup[self.skill.skill_challenge]
		atr = self.skill.skill_attribute
		operator = ""
		if rel > 0:
			operator = "+"
		if rel != 0:
			return atr.upper()+operator+str(rel)
		else:
			return atr.upper()
	def relative_value(self):
		try:
			val = 0
			if self.rank:
				  val = self.rank
			lookup = {"E":-1,"A":-2,"H":-3,"VH":-4}
			rel = val+lookup[self.skill.skill_challenge]
			atr = getattr(self.character,self.skill.skill_attribute)
			tef = 0
			traits = self.character.reladvantage.all()
			for t in traits:
				for ef in t.effect():
					if ef["effectType"] == "skillMod":
						if self.skill.skill_name in ef["skillsEffected"]:
							tef += t.rank
			return atr+rel+tef
		except Exception as e:
			return str(e)
class rel_possession(models.Model):
	ammount = models.IntegerField(default=1)
	character =     models.ForeignKey(character, on_delete=models.CASCADE, related_name='relpossession')
	possession =  models.ForeignKey(possession, on_delete=models.CASCADE, related_name='relpossession')
	def __str__(self):
		return str(self.ammount)+"x "+str(self.possession)
	def cost(self):
		return self.ammount*self.possession.possession_cost
	def weight(self):
		return self.ammount*self.possession.possession_weight
	def meleeStats(self):
		stats = self.possession.meleeStats()
		test = []
		charskills = self.character.relskill.all()
		for s in stats:
			charDam = self.character.damage()
			try:
				thisCharDam = {"die":s['damageStats']['die'], "mod":0}
			except:
				thisCharDam = charDam[s['damageStats']['stType']]
			newMod = thisCharDam['mod']+s['damageStats']['mod']
			modOpe = ""
			if newMod == 0:
				newMod = ""
			elif newMod > 0:
				modOpe = "+"
			newDam = str((thisCharDam['die']))+"d"+modOpe+str(newMod)+" "+s['damageStats']['damType'] 
			s['damage'] = newDam
			s['value'] = 0
			for cs in charskills:
				if s['skill']==cs.skill.skill_name:
					s['value'] = cs.relative_value()
		return stats
	def rangeStats(self):
		stats = self.possession.rangeStats()
		test = []
		charskills = self.character.relskill.all()
		for s in stats:
			charDam = self.character.damage()
			try:
				thisCharDam = {"die":s['damageStats']['die'], "mod":0}
			except:
				thisCharDam = charDam[s['damageStats']['stType']]
			newMod = thisCharDam['mod']+s['damageStats']['mod']
			modOpe = ""
			if newMod == 0:
				newMod = ""
			elif newMod > 0:
				modOpe = "+"
			newDam = str((thisCharDam['die']))+"d"+modOpe+str(newMod)+" "+s['damageStats']['damType']
			s['damage'] = newDam
			s['value'] = 0
			for cs in charskills:
				if s['skill']==cs.skill.skill_name:
					s['value'] = cs.relative_value()
		return stats


class rel_language(models.Model):
	character =     models.ForeignKey(character, on_delete=models.CASCADE, related_name='rellanguage')
	language =  models.ForeignKey(language, on_delete=models.CASCADE, related_name='rellanguage')
	choices = (
		(0, 'None'),
		(1, 'Broken'),
		(2, 'Accented'),
		(3, 'Fluent'),
	)
	written = models.IntegerField(choices=choices, null=True, blank=True,)
	spoken = models.IntegerField(choices=choices, null=True, blank=True,)
	def cost(self):
		if self.written and self.spoken:
			mod = 0
			if self.character.rellanguage.all()[0] == self:
				mod = -6
			return (self.written + self.spoken + mod)



class map(models.Model):
	map_name = models.CharField(max_length=255,
		verbose_name="Name",
		help_text="")
	campaign = models.ForeignKey(campaign, on_delete=models.SET_NULL, null=True, related_name="maps")
	externalHost = models.CharField(max_length=2000, blank=True, null=True,
		verbose_name="External Host",
		help_text="Web address for where map is hosted")
	image = models.ImageField(blank=True, null=True)
	maxZoom = models.IntegerField(default=0)
	startZoom = models.IntegerField(default=2)
	_middle = models.CharField(max_length=255, null=True, blank=True)
	_paths = models.CharField(max_length=9999,
		default='{"type":"FeatureCollection","features":[]}')
	def __str__(self):
		return str(self.map_name)
	def defineMaxZoom(self):
		# import json
		im = Image.open(self.image)
		w, h = im.size

		fullRes = w
		if h > w: fullRes = h
		# mid = [(fullRes/w*256),(fullRes/h*256)]
		# self._middle = json.dumps(mid)
		# maxdiv = math.ceil(fullRes/256)
		maxzoom = 0
		dyndiv = 1
		while dyndiv*2 < maxdiv:
			dyndiv = 2 ** maxzoom
			maxzoom += 1
		self.maxZoom = maxzoom+1
	def gpntile(self, Z,Y,X):
		import math
		log = []
		themap = self
		murl = themap.externalHost
		murlid = murl.split("/")[-1]
		turl = "http://tile%s.gigapan.org/gigapans0/%s/tiles/" %(murlid[:3],murlid)
		def parsetile(pos, lZ):
			z1 = 0.5
			tA = pos * z1
			t0 = math.floor(tA)
			t1 = (tA-t0)*2
			# log.append(Z)
			first = []
			# log.append({"pos":pos, "z1":z1, "tA":tA, "t0":t0, "t1":t1, })
			if lZ > 0:
				first = parsetile(t0, lZ-1)
			# log.append([z1,tA,t0,t1])
			out = first+[t1]
			return out
		
		zall = 2**Z
		if X<zall and Y<zall:
			x = parsetile(X,Z)
			y = parsetile(Y,Z)
			full = []
			for xt, yt in zip(x,y):
				full.append(str(int(xt+(2*yt))))
			
			del full[0]
			img = "".join(full)
			img = "r"+img+".jpg"
			p1 = ""
			p2 = ""
			if len(full) > 2:
				p1 = "r"+full[0]+full[1]+"/"
			if len(full) > 5:
				p2 = full[2]+full[3]+full[4]+"/"
			url = turl+p1+p2+img
			return url
	
	def paths(self):
		try:
			import json
			return json.loads(self._paths)
			# return self._paths
		except:
			return {}
	def save(self):
		if self.externalHost:
			import requests
			zrange = range(20)
			for zr in zrange:
				url = self.gpntile(zr,0,0)
				
				if requests.get(url).status_code != 200:
					break
				else:
					self.maxZoom = zr
		import math
		# self.startZoom = math.floor(self.maxZoom/2)
		# self.defineMaxZoom()
		super(map,self).save()

	class Meta:
		ordering = ['map_name']


class mapLayer(models.Model):
	parentMap = models.ForeignKey('map', on_delete=models.CASCADE, related_name="mapfeatures")
	layerName = models.CharField(max_length=255, verbose_name="Name", help_text="")
	_geoJSON = models.CharField(max_length=9999,
		default='{"type":"FeatureCollection","features":[]}')
	def geoJSON(self):
		try:
			import json
			return json.loads(self._geoJSON)
			# return self._paths
		except:
			return {}
@receiver(post_save, sender=map)
def queue_splitImage(sender, instance, created, **kwargs):
	print(instance)
	splitImage(instance.id)
	print("queued split image with id: %s" %(str(sender.id)))