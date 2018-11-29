from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib  import messages
import os
from django.conf import settings
# Create your views here.

def ortho(request):
	return render(request, "ortho.html")

def dir(request):
	# return HttpResponse(os.path.dirname(os.path.abspath(__file__)))
	return HttpResponse(settings.STATICFILES_DIRS[1])