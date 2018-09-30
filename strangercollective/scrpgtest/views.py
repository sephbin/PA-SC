from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import *
from django.contrib  import messages
# Create your views here.

def home(request):
	instance = get_object_or_404(character, id=1)
	context = {"instance":instance}
	return render(request, "rpg/home.html",context)

def card(request,characterid):
	instance = get_object_or_404(character, id=characterid)
	if request.method == "POST":
		pData = json.loads(request.POST["data"])
		# pData = {"card":"advantage"}
		lookup = {
			"attributes":{"template":"attributescard.html"},
			"advantage":{"template":"advantagecard.html"},
			"disadvantage":{"template":"disadvantagecard.html"},
		}
		context = {"instance":instance}
		return render(request, "rpg/"+lookup[pData['card']]['template'],context)