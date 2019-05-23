from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.defaultfilters import slugify
from django.contrib  import messages
from .models import *
# Create your views here.

def map(request, whatmap):
	people =	[{"label":"AB","coords":[172.125,-87.75]},{"label":"AY","coords":[171.75, -95.625]}]
	context =	{"whatmap":whatmap}
	return render(request, "maps/officemap.html", context)