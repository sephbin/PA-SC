from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import *
from django.contrib  import messages
# Create your views here.

def home(request):
	instance = get_object_or_404(character, id=1)
	context = {"instance":instance}
	return render(request, "rpg/home.html",context)

def advantagecard(request,characterid):
	instance = get_object_or_404(character, id=characterid)
	context = {"instance":instance}
	if request.method == "POST":
		return render(request, "rpg/advantagecard.html",context)
	else:
		return render(request, "rpg/advantagecard.html",context)
