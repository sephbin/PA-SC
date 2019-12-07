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

def login_view(request):
	from django.contrib.auth import login
	from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
	print("LOGIN_VIEW")
	if request.method == "POST":
		print(request.POST)
		try:
			request.POST["password"]
			form = AuthenticationForm(data=request.POST)
			if form.is_valid():
				#log in the user
				user = form.get_user()
				login(request,user)
				if 'next' in request.POST:
					return HttpResponseRedirect(request.POST.get("next"))
				else:
					return HttpResponseRedirect("/rpg")
			else:
				signup_form = UserCreationForm()
				context = {
							'first':'login',
							'login_form':form,
							'signup_form':signup_form,
							'next':request.GET.get('next')}
				return render(request, "crowbar/login.html", context)
		except:
			form = UserCreationForm(request.POST)
			if form.is_valid():
				user = form.save()
				# log the user in
				login(request,user)
				if 'next' in request.POST:
					return HttpResponseRedirect(request.POST.get("next"))
				else:
					return HttpResponseRedirect("/rpg")
			else:
				login_form = AuthenticationForm()
				context = {
							'first':'signup',
							'login_form':login_form,
							'signup_form':form,
							'next':request.GET.get('next')}
				return render(request, "crowbar/login.html", context)
	if request.method == "GET":
		login_form = AuthenticationForm()
		signup_form = UserCreationForm()
	context = {
				'first':'login',
				'login_form':login_form,
				'signup_form':signup_form,
				'next':request.GET.get('next')}
	return render(request,"crowbar/login.html",context)

def signup_view(request):
	from django.contrib.auth import login
	from django.contrib.auth.forms import UserCreationForm
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			# log the user in
			login(request,user)
			if 'next' in request.POST:
				return HttpResponseRedirect(request.POST.get("next"))
			else:
				return HttpResponseRedirect("/")
		else:
			for e in form.errors:
				print(type(e))
				# print(dir(e))
			context = {"form":form}
			return render(request, "crowbar/login.html", context)

	else:
		form = UserCreationForm()
	context = {"form":form}
	return render(request, "crowbar/signup.html", context)
def logout_view(request):
	from django.contrib.auth import logout
	logout(request)
	return HttpResponseRedirect("/rpg")
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
def home(request):
	context = {}
	return render(request, "crowbar/home.html", context)

@login_required(login_url="/rpg/login/")
def createCampaign(request):
	from django.forms import ModelForm
	class CampaignForm(ModelForm):
		class Meta:
			model = campaign
			# fields = '__all__'
			fields = ['name']
	if request.method == "POST":
		form = CampaignForm(data=request.POST)
		if form.is_valid():
			nuob = form.save(commit=False)
			nuob.save()
			form.save_m2m()
			nuob.gameMaster.add(request.user)
			return HttpResponseRedirect("/rpg")
		else:
			return JsonResponse({
			"valid":form.is_valid(),
				})
	if request.method == "GET": 
		form = CampaignForm()
		context = {"form":form,
		"model": "Campaign",
		}
		return render(request, "crowbar/createForm.html", context)

@login_required(login_url="/rpg/login/")
def CRUDMap(request, whatCampaign, whatMap = None):
	from django.forms import ModelForm
	if whatMap:
		instance = get_object_or_404(map, id=whatMap)
	if request.user.username != "sephbin":
		class MapForm(ModelForm):
			class Meta:
				model = map
				# fields = '__all__'
				fields = ['map_name', 'externalHost',]
	else:
		class MapForm(ModelForm):
			class Meta:
				model = map
				# fields = '__all__'
				fields = ['map_name', 'externalHost', 'image', 'maxZoom','startZoom']
	
	thecampaign = get_object_or_404(campaign, id=int(whatCampaign))
	accessList = []
	gms = thecampaign.gameMaster.all()
	for g in gms:		accessList.append(g)

	user = request.user
	if user in accessList:
		if request.method == "POST":
			if whatMap:
				form = MapForm(request.POST, request.FILES, instance=instance)
			else:
				form = MapForm(request.POST, request.FILES)
			if form.is_valid():
				nuob = form.save(commit=False)
				nuob.campaign = thecampaign
				nuob.save()
				form.save_m2m()
				return HttpResponseRedirect("/rpg")
			else:
				return JsonResponse({
				"valid":form.is_valid(),
				"errors": form.errors,
					})
		if request.method == "GET": 
			if whatMap:
				form = MapForm(instance=instance)
			else:	
				form = MapForm()
			context = {"form":form,
			"model": "Map",
			}
			return render(request, "crowbar/createForm.html", context)
	else:
		return JsonResponse({
				"error":"No campaign matches the given query.",
					})

# @user_passes_test(teacher_check)

# @login_required(login_url="/rpg/login/")
@csrf_exempt
def editmappaths(request, whatmap):
	if request.method == "POST":
		try:
			import json
			d = json.loads(request.POST["data"])
			mapinstance = get_object_or_404(map, id=whatmap)
			print(d)
			print(mapinstance)
			mapinstance._paths = json.dumps(d)
			mapinstance.save()
			return JsonResponse({"isError":False})
		except:
			return JsonResponse({"isError":True})

@login_required(login_url="/rpg/login/")
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

def externaltile(request,mapid,Z,Y,X):
	themap = get_object_or_404(map, id=mapid)
	url = themap.gpntile(Z,Y,X)
	return HttpResponseRedirect(url)
	
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
