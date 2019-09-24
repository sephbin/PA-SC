from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib  import messages
from .models import *
# Create your views here.

def index(request, id):
	instance = get_object_or_404(rb_item, id=id)
	# queryset = rb_item.objects.all()
	# queryset = queryset[::-1]
	# queryset.remove(instance)
	# queryset = queryset[:3]
	context = {
	"instance": instance,
	}

	return render(request, "redback-index.html", context)

def three(request):
	context = {}
	return render(request, "redback/three-example.html", context)