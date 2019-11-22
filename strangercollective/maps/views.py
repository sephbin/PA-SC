from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.defaultfilters import slugify
from django.contrib  import messages
from .models import *
# Create your views here.

def mapview(request, whatmap):
	markers = [
	{"title":"Large Logging Camp", "icon":"hatchet.svg", "coords":[ 143.25, -100.875 ]},
	{"title":"Large Logging Camp", "icon":"hatchet.svg", "coords":[ 118, -81.25 ]},
	{"title":"Large Logging Camp", "icon":"hatchet.svg", "coords":[ 86.25, -106.625 ]},
	]
	themap = get_object_or_404(map,map_name=whatmap)
	context =	{"whatmap":whatmap, "markers": markers, "map":themap}
	return render(request, "maps/officemap.html", context)