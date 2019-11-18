from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib  import messages
from .models import *
# Create your views here.
from rest_framework import viewsets
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def getPayload(request, log = []):
	import json
	d = {}
	try:
		d = json.loads(str(request.body, encoding='utf-8'))
	except Exception as e:
		log.append(str(e))
		if request.method == "GET":
			try:	d = dict(request.GET)
			except: pass
		if request.method == "POST":
			try:
				d = json.loads(str(request.body, encoding='utf-8'))
				log.append(str("getPayload try worked"))
				log.append(str(d))
			except:
				d = dict(request.POST)
				log.append(str("getPayload except"))
				log.append(str(d))
		if request.method == "DELETE":
			try:	d = json.loads(str(request.body, encoding='utf-8'))
			except: pass
	try:
		d = json.loads(d["data"][0])
	except: pass
	try:
		for i in d:
			i = json.loads(i)
	except: pass
	log.append(str("getPayload"))
	log.append(str(d))
	return d

class ParameterViewSet(viewsets.ModelViewSet):
    queryset = parameterObject.objects.all()
    serializer_class = ParameterObSerializer


def familygetscript(request, familyname, scripttype = "gh"):
	instance = get_object_or_404(family, name=familyname)
	
	return HttpResponse(instance.gh_script)

@csrf_exempt
def create_update_parameter(request):
	log = []
	if request.method == "POST":
		payloads = getPayload(request, log)
		try:
			for payload in payloads:
				try:
					log.append(payload)
					existing = get_object_or_404(parameterObject, parameterIdentity=payload["parameterIdentity"])
					serializer = ParameterObSerializer_CU(existing, data=payload)
					log.append("try worked")
				except Exception as e:
					log.append(str(e))
					serializer = ParameterObSerializer_CU(data=payload)
				log.append(serializer.is_valid())
				if serializer.is_valid():
					savedObject = serializer.save()
					log.append("created or updated %s" %(str(savedObject)))
		except Exception as e:
			log.append(str(e))
		return JsonResponse({
			"log":log,
		})
	else:
		return HttpResponse("NOT POST")

@csrf_exempt
def create_update_map(request):
	log = []
	if request.method == "POST":
		payload = getPayload(request, log)
		payload["object_from"] = get_object_or_404(parameterObject, parameterIdentity=payload["object_from"])
		payload["object_to"] = get_object_or_404(parameterObject, parameterIdentity=payload["object_to"])

		object, created = parameterMapThroughObject.objects.update_or_create(
			object_from = payload["object_from"], object_to = payload["object_to"], function = payload["function"], defaults = payload)
		if created:
			log.append("Created %s" %(str(object)))
		else:
			log.append("Updated %s" %(str(object)))
		return JsonResponse({
			"log":log,		
			})
	else:
		return HttpResponse("NOT POST")

