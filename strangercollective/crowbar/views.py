from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from .models import *
# from .serializers import *
# Create your views here.
def getPage(request, url):
	import requests
	from bs4 import BeautifulSoup
	page = url.replace("__","/")
	if "://" not in page:
		page = "http://"+request.META['HTTP_HOST']+page
	page_contents = BeautifulSoup(requests.get(page).text, features="lxml")
	page_contents = str(page_contents.find('body').decode_contents())
	return page_contents

@csrf_exempt
def splitPage(request,pformat="splitPage", left=None, right=None, center=None):
	log = []
	isError = False
	if request.method == "GET":
		if left:
			left = getPage(request, left)
		if right:
			right = getPage(request, right)
		if center:
			center = getPage(request, center)


		context = {"left":left,"right":right,"center":center}
		return render(request,"crowbar/layouts/%s.html"%(pformat),context)
	if request.method == "POST":
		print(request.POST)
		page = getPage(request, request.POST["href"])
		return JsonResponse({"isError":isError,"log":log,"page":page})


@csrf_exempt
def charContent(request, charID=None, page="1"):
	instance = get_object_or_404(character, id=charID)
	if request.method == "GET":
		data = instance.gcaData
		data["Attributes"]= {}
		# attributes = ["ST","DX","IQ","HT", "HP","Will","Per","FP",]
		
		for a in data["Traits"]["Attribute"]:
			try:
				# if a["symbol"] in attributes:
				data["Attributes"][a["symbol"].replace(" ","_")] = a
			except: pass
			try:
				# if a["name"] in attributes:
				data["Attributes"][a["name"].replace(" ","_")] = a
			except: pass
		for k in data["Traits"]:
			if type(data["Traits"][k]) == type({}):
				data["Traits"][k] = [data["Traits"][k]]
		
		if "Spell" not in data["Traits"]:
			data["Traits"]["Spell"] = []
		data["Traits"]["All"] = data["Traits"]["Equipment"]+data["Traits"]["Advantage"]+data["Traits"]["Spell"]+data["Traits"]["Skill"]
		data["Block"] = 0
		for eq in data["Traits"]["All"]:
			if "blocklevel" in eq:
				if data["Block"] < int(eq["blocklevel"]):
					data["Block"] = eq["blocklevel"]
			try:
				eq["damages"] = []
				rootDM = eq["damage"].split("|")
				for rD in rootDM:
					eq["damages"].append({})
				for k,v in eq.items():
					# print(k,v)
					try:
						if "|" in v:
							dmindex = 0
							for sv in v.split("|"):
								eq["damages"][dmindex][k] = sv
								dmindex += 1
						else:
							if k != "damages":
								eq["damages"][0][k] = v
					except: pass
				delindexs = []
				delindex = 0
				for mode in eq["damages"]:
					if "DX" in mode["charskillused"]:
						delindexs.append(delindex)
					delindex += 1
				for di in reversed(delindexs):
					del eq["damages"][di]
			except: pass
		context = {"instance":data}
		return render(request,"crowbar/content/simpleChar%s.html"%(page),context)