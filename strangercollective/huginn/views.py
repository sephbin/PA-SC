from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib  import messages
from .models import *
# Create your views here.
from rest_framework import viewsets
from .serializers import *
# Create your views here.
class ParameterViewSet(viewsets.ModelViewSet):
    queryset = parameterOb.objects.all()
    serializer_class = ParameterObSerializer


def familygetscript(request, familyname, scripttype = "gh"):
	instance = get_object_or_404(family, name=familyname)
	
	return HttpResponse(instance.gh_script)

