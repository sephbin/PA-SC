from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib  import messages
# Create your views here.

def ortho(request):
	return render(request, "ortho.html")

