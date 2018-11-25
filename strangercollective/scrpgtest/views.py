from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import *
from django.contrib  import messages
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def home(request):
	instance = get_object_or_404(character, id=1)
	context = {"instance":instance}
	return render(request, "rpg/home.html",context)

def characterlist(request):
	user = request.user
	chars = character.objects.all()
	context = {"characterList":[]}
	for c in chars:
		abop = {"name":str(c),"id":c.id}
		context["characterList"].append(abop)
	abop = {"name":str(user),"id":0}
	context["characterList"].append(abop)
	return JsonResponse(context)

def characterdata(request, characterid):
	ins = get_object_or_404(character, id=characterid)
	context = {
	"attributes"	: {
	"st":ins.st,
	"dx":ins.dx,
	"iq":ins.iq,
	"ht":ins.ht,
	"hp":ins.hp,
	"will":ins.will,
	"per":ins.per ,
	"fp":ins.fp,
	"sm":ins.sm,
	"bs":ins.bs,
	"bm":ins.bm,
	},
	"advantages"	: [],
	"disadvantages"	: [],
	"skills"		: [],
	"languages"		: [],
	"possessions"	: [],
	"possessionsTotals": {"cost": 0, "weight": 0},
	"melee"		: [],
	"ranged"		: [],
	}
	for i in ins.reladvantage.all():
		apob = {}
		apob["name"] = str(i.name())
		apob["cost"] = i.cost()
		context["advantages"].append(apob)
	for i in ins.reldisadvantage.all():
		apob = {}
		apob["name"] = str(i.disadvantage)
		apob["cost"] = i.cost()
		context["disadvantages"].append(apob)
	for i in ins.relskill.all():
		apob = {}
		apob["name"] = str(i.skill)
		apob["challenge"] = i.skill_challenge()
		apob["relative"] = i.relative_skill()
		apob["value"] = i.relative_value()
		apob["cost"] = i.cost()
		context["skills"].append(apob)
	for i in ins.rellanguage.all():
		apob = {}
		apob["language"] = str(i.language)
		apob["written"] = i.choices[i.written][1]
		apob["spoken"] = i.choices[i.spoken][1]
		apob["cost"] = i.cost()
		context["languages"].append(apob)
	for i in ins.relpossession.all():
		apob = {}
		apob["name"] = str(i.possession)
		apob["ammount"] = i.ammount
		apob["weight"] = i.weight()
		context["possessionsTotals"]["weight"] += i.weight()
		apob["cost"] = i.cost()
		context["possessionsTotals"]["cost"] += i.cost()
		context["possessions"].append(apob)
		if i.possession.meleeStatsText:
			apob = {}
			apob["name"] = str(i.possession)
			apob["meleestats"] = i.meleeStats()
			context["melee"].append(apob)
		if i.possession.rangeStatsText:
			apob = {}
			apob["name"] = str(i.possession)
			apob["rangestats"] = i.rangeStats()
			context["ranged"].append(apob)
	return JsonResponse(context)

@csrf_exempt
def card(request,characterid):
	instance = get_object_or_404(character, id=characterid)
	if request.method == "POST":
		pData = json.loads(request.POST["data"])
		# pData = {"card":"advantage"}
		lookup = {
			"attributes":{"template":"attributescard.html"},
			"advantage":{"template":"advantagecard.html"},
			"disadvantage":{"template":"disadvantagecard.html"},
		}
		context = {"instance":instance}
		return render(request, "rpg/"+lookup[pData['card']]['template'],context)
	else:
		context = {"instance":instance}
		return JsonResponse({"advantages":[{"name":"Fit","cost":5},{"name":"Very Fit","cost":15},{"name":"Innate Attack (Aura, 50%)","cost":5}],"disadvantages":[{"name":"Not Fit","cost":-5},{"name":"Not Very Fit","cost":-15},{"name":"Shitty Innate Attack (Aura, 50%)","cost":-5}]})
