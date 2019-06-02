from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.defaultfilters import slugify
from django.contrib  import messages
from .models import *
# Create your views here.

def map(request, whatmap):
	markers = [
	{"title":"Large Logging Camp", "icon":"hatchet.svg", "coords":[ 143.25, -100.875 ]},
	{"title":"Large Logging Camp", "icon":"hatchet.svg", "coords":[ 118, -81.25 ]},
	{"title":"Large Logging Camp", "icon":"hatchet.svg", "coords":[ 86.25, -106.625 ]},
	]
	context =	{"whatmap":whatmap, "markers": markers}
	return render(request, "maps/officemap.html", context)