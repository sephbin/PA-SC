from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from .models import *

# Create your views here.
def clock(request):
	context = {}
	return render(request, "changeling/clock.html", context)