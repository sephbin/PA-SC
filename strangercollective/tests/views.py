from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib  import messages
import os
from django.conf import settings
from .models import *
from .serializers import *
# Create your views here.

def ortho(request, m= "first"):
	tmap = get_object_or_404(tokenmap, name=m)
	tokens = tmap.tokens.all()
	context = {
	"tokens":json.dumps(TokenSerializer(tokens, many=True).data),
	"map":tmap,
	"updated": tmap.updated.strftime("%Y%m%d%H%M%S%f"),
	}
	print(context)
	print(tmap.updated.strftime("%Y%m%d%H%M%S"))
	return render(request, "ortho.html", context)

def tokenpos(request, id, x, y, z):
	t = get_object_or_404(token, id=id)
	t.position = {"x":float(x), "y":float(y), "z":float(z)}
	t.save()
	return JsonResponse({"error":False})

def ismapupdated(request, id, date):
	from datetime import datetime
	import pytz
	utc= pytz.timezone('Etc/Greenwich')
	date = utc.localize(datetime.strptime(date, "%Y%m%d%H%M%S%f"))
	# date = datetime.strptime(date, "%Y%m%d%H%M%S")
	tmap = get_object_or_404(tokenmap, id=id)
	# print(date,tmap.updated)
	if date < tmap.updated:
		tokens = TokenSerializer(tmap.tokens.filter(updated__gte=date), many=True).data
		return JsonResponse({"error":False, "updated":True,"edit":tokens, "updatedtime":tmap.updated.strftime("%Y%m%d%H%M%S%f")})
	else:
		return JsonResponse({"error":False, "updated":False})
def dir(request):
	# return HttpResponse(os.path.dirname(os.path.abspath(__file__)))
	return HttpResponse(settings.STATICFILES_DIRS)

def table(request):
	return render(request, "table.html")