from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *

# Create your views here.
def panoramaview(request,colle,pano):
	v_collection = collection.objects.get(collection_name=colle)
	p_collection = v_collection.panorama.all()
	p_collection = list(map(lambda x: x, p_collection))
	instance = panorama.objects.get(panorama_name=pano)
	currentindex = p_collection.index(instance)
	lastItem = p_collection[(currentindex-1) % len(p_collection)]
	nextItem = p_collection[(currentindex+1) % len(p_collection)]
	print(currentindex)
	context = { "context": instance, "last":lastItem, "next":nextItem }
	if instance.cubemap and not instance.stereoscopic:
		return render(request, "panorama/aframe-cm-m.html", context)