from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *

# Create your views here.
def panoramaview(request,collection,pano):
	instance = panorama.objects.get(panorama_name=pano)
	context = { "context": instance }
	return render(request, "panorama/m-stereo.html", context)