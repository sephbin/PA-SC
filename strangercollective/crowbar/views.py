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
def splitPage(request,pformat="splitPage", char=None, left=None, right=None, center=None):
	log = []
	isError = False
	if request.method == "GET":
		if left:
			left = getPage(request, left)
		if right:
			right = getPage(request, right)
		if center:
			center = getPage(request, center)


		context = {"char":char, "left":left,"right":right,"center":center}
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
		
		dr = {
			"skull": [2+int(data["Attributes"]["DR"]["score"]),2+int(data["Attributes"]["DR"]["score"])],
			"neck": [int(data["Attributes"]["DR"]["score"]),int(data["Attributes"]["DR"]["score"])],
			"face": [int(data["Attributes"]["DR"]["score"]),int(data["Attributes"]["DR"]["score"])],
			"eyes": [0,0],
			"torso": [int(data["Attributes"]["DR"]["score"]),int(data["Attributes"]["DR"]["score"])],
			"groin": [int(data["Attributes"]["DR"]["score"]),int(data["Attributes"]["DR"]["score"])],
			"feet": [int(data["Attributes"]["DR"]["score"]),int(data["Attributes"]["DR"]["score"])],
			"arms": [int(data["Attributes"]["DR"]["score"]),int(data["Attributes"]["DR"]["score"])],
			"legs": [int(data["Attributes"]["DR"]["score"]),int(data["Attributes"]["DR"]["score"])],
			"hands": [int(data["Attributes"]["DR"]["score"]),int(data["Attributes"]["DR"]["score"])],
		}
		for tr in data["Traits"]["All"]:
			try:
				if "chardr" in tr:
					drs = tr["chardr"].replace("*","").split("/")
					drs = list(map(lambda x: int(x), drs))
					if len(drs) == 1:
						drs = [drs[0],drs[0]]
					# print("drs",drs)
					locs = tr["location"].lower().split(", ")
					for l in locs:
						index = 0
						for a,b in zip(dr[l],drs):
							dr[l][index] = a+b
							index += 1
			except Exception as e:
				# print(e)
				pass
		# print(dr)
		for k, v in dr.items():
			v = list(map(lambda x: str(x), v))
			if v[0]==v[1]:
				dr[k] = v[0]
			else:
				print(k,v)
				dr[k] = "/".join(v)


		context = {"instance":data, "dr":dr}
		return render(request,"crowbar/content/simpleChar%s.html"%(page),context)