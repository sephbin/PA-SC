from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, render
from django.contrib  import messages
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets

from .models import *
from .serializers import *
# Create your views here.
class CharacterViewSet(viewsets.ModelViewSet):
    queryset = character.objects.all()
    serializer_class = CharacterSerializer

class RaceViewSet(viewsets.ModelViewSet):
    queryset = race.objects.all()
    serializer_class = raceSerializer

class PossessionViewSet(viewsets.ModelViewSet):
    queryset = possession.objects.all()
    serializer_class = PossessionSerializer

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = campaign.objects.all()
    serializer_class = CampaignSerializer

def charPage(request, characterid):
	instance = get_object_or_404(character, id=characterid)
	context = {"instance":instance }
	return render(request, "crowbar/base.html",context)

def csCard(request, characterid, cardid):
	instance = get_object_or_404(character, id=characterid)
	context = {"instance":instance }
	return render(request, "crowbar/"+cardid+".html",context)

def editattr(request, characterid, attrid, attrval):
	instance = character.objects.get(id=characterid)
	instance.__setattr__(attrid, float(attrval))
	instance.save()
	newinstance = character.objects.get(id=characterid)
	context = {"instance":newinstance, "show":True}
	return render(request, "crowbar/modal-Attributes.html", context)

def newpos(request, characterid, possessionid):
	instance = character.objects.get(id=characterid)
	item = possession.objects.get(id=possessionid)
	charpos = instance.relpossession.all()
	new = True
	for cp in charpos:
		if cp.possession == item:
			cp.ammount += 1
			cp.save()
			new = False
	if new:
		q = rel_possession(ammount=1, character=instance, possession=item)
		q.save()
	newinstance = character.objects.get(id=characterid)
	context = {"instance":newinstance, "show":True}
	return render(request, "crowbar/modal-Possession.html", context)


def editskill(request, characterid, skillid, rank):
	instance = rel_skill.objects.get(id=skillid)
	instance.rank = int(rank)
	instance.save()
	newchar = character.objects.get(id=characterid)
	context = {"instance":newchar, "show":True}
	return render(request, "crowbar/modal-Skill.html", context)

def remskill(request, characterid, skillid):
	relskill = rel_skill.objects.get(id=skillid)
	relskill.delete()
	newinstance = character.objects.get(id=characterid)
	context = {"instance":newinstance, "show":True}
	return render(request, "crowbar/modal-Skill.html", context)

def newskill(request, characterid, skillid):
	instance = character.objects.get(id=characterid)
	newskill = skill.objects.get(id=skillid)
	new = rel_skill()
	new.character = instance
	new.skill = newskill
	new.rank = 1
	new.save()
	newinstance = character.objects.get(id=characterid)
	context = {"instance":newinstance, "show":True}
	return render(request, "crowbar/modal-Skill.html", context)

def newadvantage(request, characterid, traitid):
	instance = character.objects.get(id=characterid)
	newadvantage = advantage.objects.get(id=traitid)
	new = rel_advantage()
	new.character = instance
	new.advantage = newadvantage
	new.save()
	newinstance = character.objects.get(id=characterid)
	context = {"instance":newinstance, "show":True}
	return render(request, "crowbar/modal-Advantage.html", context)

def remadvantage(request, characterid, traitid):
	reladv = rel_advantage.objects.get(id=traitid)
	reladv.delete()
	newinstance = character.objects.get(id=characterid)
	context = {"instance":newinstance, "show":True}
	return render(request, "crowbar/modal-Advantage.html", context)

def ediadvantagemodal(request, characterid, traitid):
	reladv = rel_advantage.objects.get(id=traitid)
	context = {"instance": reladv}
	return render(request, "crowbar/modal-EditAdvantage.html", context)

def rempos(request, characterid, possessionid):
	instance = character.objects.get(id=characterid)
	item = possession.objects.get(id=possessionid)
	charpos = instance.relpossession.all()
	for cp in charpos:
		if cp.possession == item:
			cp.ammount += -1
			if cp.ammount == 0:
				cp.delete()
			else:
				cp.save()
	newinstance = character.objects.get(id=characterid)
	context = {"instance":newinstance, "show":True}
	return render(request, "crowbar/modal-Possession.html", context)

# def teacher_check(user):
# 	groups = user.groups.all()
# 	groups = list(map(lambda x: x.name, groups))
# 	test = "UNSW_TEACHER" in groups
# 	return test

@login_required(login_url="/rpg/login/")
# @user_passes_test(teacher_check)
def mapview(request, whatmap):
	
	themap = get_object_or_404(map, id=whatmap)
	accessList = []
	gms = themap.campaign.gameMaster.all()
	players = themap.campaign.player.all()
	for g in gms:		accessList.append(g)
	for g in players:	accessList.append(g)

	user = request.user
	if user in accessList: 
		markers = []
		context =	{"whatmap":whatmap, "markers": markers, "map":themap}
		return render(request, "maps/map.html", context)
	else:
		return JsonResponse({"error":"No map found!"})
# def home(request):
# 	instance = get_object_or_404(character, id=1)
# 	context = {"instance":instance}
# 	return render(request, "rpg/home.html",context)

# def characterlist(request):
# 	user = request.user
# 	chars = character.objects.all()
# 	context = {"characterList":[]}
# 	for c in chars:
# 		abop = {"name":str(c),"id":c.id}
# 		context["characterList"].append(abop)
# 	abop = {"name":str(user),"id":0}
# 	context["characterList"].append(abop)
# 	return JsonResponse(context)

# def characterdata(request, characterid):
# 	ins = get_object_or_404(character, id=characterid)
# 	context = {
# 	"attributes"	: {
# 	"st":ins.st,
# 	"dx":ins.dx,
# 	"iq":ins.iq,
# 	"ht":ins.ht,
# 	"hp":ins.hp,
# 	"will":ins.will,
# 	"per":ins.per ,
# 	"fp":ins.fp,
# 	"sm":ins.sm,
# 	"bs":ins.bs,
# 	"bm":ins.bm,
# 	},
# 	"advantages"	: [],
# 	"disadvantages"	: [],
# 	"skills"		: [],
# 	"languages"		: [],
# 	"possessions"	: [],
# 	"possessionsTotals": {"cost": 0, "weight": 0},
# 	"melee"		: [],
# 	"ranged"		: [],
# 	}
# 	for i in ins.reladvantage.all():
# 		apob = {}
# 		apob["name"] = str(i.name())
# 		apob["cost"] = i.cost()
# 		context["advantages"].append(apob)
# 	for i in ins.reldisadvantage.all():
# 		apob = {}
# 		apob["name"] = str(i.disadvantage)
# 		apob["cost"] = i.cost()
# 		context["disadvantages"].append(apob)
# 	for i in ins.relskill.all():
# 		apob = {}
# 		apob["name"] = str(i.skill)
# 		apob["challenge"] = i.skill_challenge()
# 		apob["relative"] = i.relative_skill()
# 		apob["value"] = i.relative_value()
# 		apob["cost"] = i.cost()
# 		context["skills"].append(apob)
# 	for i in ins.rellanguage.all():
# 		apob = {}
# 		apob["language"] = str(i.language)
# 		apob["written"] = i.choices[i.written][1]
# 		apob["spoken"] = i.choices[i.spoken][1]
# 		apob["cost"] = i.cost()
# 		context["languages"].append(apob)
# 	for i in ins.relpossession.all():
# 		apob = {}
# 		apob["name"] = str(i.possession)
# 		apob["ammount"] = i.ammount
# 		apob["weight"] = i.weight()
# 		context["possessionsTotals"]["weight"] += i.weight()
# 		apob["cost"] = i.cost()
# 		context["possessionsTotals"]["cost"] += i.cost()
# 		context["possessions"].append(apob)
# 		if i.possession.meleeStatsText:
# 			apob = {}
# 			apob["name"] = str(i.possession)
# 			apob["meleestats"] = i.meleeStats()
# 			context["melee"].append(apob)
# 		if i.possession.rangeStatsText:
# 			apob = {}
# 			apob["name"] = str(i.possession)
# 			apob["rangestats"] = i.rangeStats()
# 			context["ranged"].append(apob)
# 	return JsonResponse(context)

# @csrf_exempt
# def card(request,characterid):
# 	instance = get_object_or_404(character, id=characterid)
# 	if request.method == "POST":
# 		pData = json.loads(request.POST["data"])
# 		# pData = {"card":"advantage"}
# 		lookup = {
# 			"attributes":{"template":"attributescard.html"},
# 			"advantage":{"template":"advantagecard.html"},
# 			"disadvantage":{"template":"disadvantagecard.html"},
# 		}
# 		context = {"instance":instance}
# 		return render(request, "rpg/"+lookup[pData['card']]['template'],context)
# 	else:
# 		context = {"instance":instance}
# 		return JsonResponse({"advantages":[{"name":"Fit","cost":5},{"name":"Very Fit","cost":15},{"name":"Innate Attack (Aura, 50%)","cost":5}],"disadvantages":[{"name":"Not Fit","cost":-5},{"name":"Not Very Fit","cost":-15},{"name":"Shitty Innate Attack (Aura, 50%)","cost":-5}]})
