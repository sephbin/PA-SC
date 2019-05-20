from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.defaultfilters import slugify
from django.contrib  import messages
from .models import *
# Create your views here.

def map(request):
	people = [{"label":"AB","coords":[172.125,-87.75]},{"label":"AY","coords":[171.75, -95.625]}]
	context = {"polygons":[
	{"coords":[[100, -100], [100, -120], [80, -120], [80, -100]], "color": 'green', "stroke": False, "fillOpacity": 0.8, },
	],"people":people}
	return render(request, "maps/officemap.html", context)