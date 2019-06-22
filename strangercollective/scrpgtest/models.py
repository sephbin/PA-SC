from django.db import models
import math
import json
import requests
# from django.contrib.auth.models import User
# from taggit.managers import TaggableManager
# Create your models here.

class campaign(models.Model):
    name = models.CharField(max_length = 120)
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
    def __str__(self):
        return self.skill_name
class possession(models.Model):
    campaign = models.ManyToManyField(campaign, related_name="possession")
    possession_name = models.CharField(max_length=120)
    possession_description = models.TextField(max_length = 9999, blank=True, null=True)
    possession_weight = models.IntegerField(default=0)
    possession_cost = models.IntegerField(default=0)
    ####WEAPONS ARMOURS ETC ####
    meleeStatsText = models.TextField(max_length = 9999, blank=True, null=True)
    rangeStatsText = models.TextField(max_length = 9999, blank=True, null=True)
    armourStatsText = models.TextField(max_length = 9999, blank=True, null=True)
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
    def damage(self):
        lookup = {"1":{"Thrust":{"die":1,"mod":-6},"Swing":{"die":1,"mod":-5}},"2":{"Thrust":{"die":1,"mod":-6},"Swing":{"die":1,"mod":-5}},"3":{"Thrust":{"die":1,"mod":-5},"Swing":{"die":1,"mod":-4}},"4":{"Thrust":{"die":1,"mod":-5},"Swing":{"die":1,"mod":-4}},"5":{"Thrust":{"die":1,"mod":-4},"Swing":{"die":1,"mod":-3}},"6":{"Thrust":{"die":1,"mod":-4},"Swing":{"die":1,"mod":-3}},"7":{"Thrust":{"die":1,"mod":-3},"Swing":{"die":1,"mod":-2}},"8":{"Thrust":{"die":1,"mod":-3},"Swing":{"die":1,"mod":-2}},"9":{"Thrust":{"die":1,"mod":-2},"Swing":{"die":1,"mod":-1}},"10":{"Thrust":{"die":1,"mod":-2},"Swing":{"die":1,"mod":0}},"11":{"Thrust":{"die":1,"mod":-1},"Swing":{"die":1,"mod":1}},"12":{"Thrust":{"die":1,"mod":-1},"Swing":{"die":1,"mod":2}},"13":{"Thrust":{"die":1,"mod":0},"Swing":{"die":2,"mod":-1}},"14":{"Thrust":{"die":1,"mod":0},"Swing":{"die":2,"mod":0}},"15":{"Thrust":{"die":1,"mod":1},"Swing":{"die":2,"mod":1}},"16":{"Thrust":{"die":1,"mod":1},"Swing":{"die":2,"mod":2}},"17":{"Thrust":{"die":1,"mod":2},"Swing":{"die":3,"mod":-1}},"18":{"Thrust":{"die":1,"mod":2},"Swing":{"die":3,"mod":0}},"19":{"Thrust":{"die":2,"mod":-1},"Swing":{"die":3,"mod":1}},"20":{"Thrust":{"die":2,"mod":-1},"Swing":{"die":3,"mod":2}}}
        damkey = str(self.st)
        return(lookup[damkey])
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
        "bsCost":((self.bs*4)-(self.ht+self.dx))*5,
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
        return tally
    def save(self, *args, **kwargs):
        super(character, self).save(*args, **kwargs)
        payload = {'value1': self.firstname+" "+self.lastname+" ["+str(self.cost())+"]", 'value2': 'http://www.strangercollective.com/rpg/'+str(self.id)}
        try:
            r = requests.post("https://maker.ifttt.com/trigger/crowbarcharacteredit/with/key/bhFn8UCEstaDR_dRNGLoBd", data=payload)
        except:
            pass


class modPackage(models.Model):
    # relAdv = models.ForeignKey(rel_advantage, on_delete=models.CASCADE)
    # packageName = models.CharField(max_length = 120)
    # modifiers = models.ForeignKey(modifier, on_delete=models.CASCADE,null=True,blank=True,)
    def __str__(self):
        mods = self.modifier_set.all()
        txt = []
        for i in mods:
            txt.append(str(i))
        txt = "; ".join(txt)
        return txt

class modifier(models.Model):
    modPackage = models.ForeignKey(modPackage, on_delete=models.CASCADE)
    name = models.CharField(max_length = 120)
    description = models.CharField(max_length = 120)
    modifier = models.IntegerField()
    def __str__(self):
        return self.name

class rel_advantage(models.Model):
    character = models.ForeignKey(character, on_delete=models.CASCADE, related_name='reladvantage')
    advantage = models.ForeignKey(advantage, on_delete=models.CASCADE, related_name='reladvantage')
    modifiers = models.ForeignKey(modPackage, on_delete=models.CASCADE,null=True,blank=True,)
    # modifiers = models.ManyToManyField(modifier, blank=True,)
    rank = models.IntegerField(null=True, blank=True,)
    def mods(self):
        return self.modifiers
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
    modifiers = models.ForeignKey(modPackage, on_delete=models.CASCADE,null=True,blank=True,)
    # modifiers = models.ManyToManyField(modifier, blank=True,)
    rank = models.IntegerField(null=True, blank=True,)
    def mods(self):
        return self.modifiers
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
    def cost(self):
        if self.rank:
            if self.rank < 3:
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
        lookup = {"E":0,"A":-1,"H":-2,"VH":-3}
        rel = val+lookup[self.skill.skill_challenge]
        atr = self.skill.skill_attribute
        operator = ""
        if rel > 0:
            operator = "+"
        if rel != 0:
            return atr.upper()+operator+str(rel)
        else:
            return atr
    def relative_value(self):
        try:
            val = 0
            if self.rank:
                  val = self.rank
            lookup = {"E":0,"A":-1,"H":-2,"VH":-3}
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