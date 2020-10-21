from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from .models import *
# from .serializers import *
# Create your views here.
def getPage(request, url):
	import requests
	from bs4 import BeautifulSoup
	page = url.replace("__","/")
	if "://" not in page:
		page = "http://"+request.META['HTTP_HOST']+page
	page_contents = BeautifulSoup(requests.get(page).text, features="lxml")
	page_contents = str(page_contents.find('body').decode_contents())
	return page_contents

@csrf_exempt
def splitPage(request, left=None, right=None):
	log = []
	isError = False
	if request.method == "GET":
		if left:
			left = getPage(request, left)
		if right:
			right = getPage(request, right)

		context = {"left":left,"right":right}
		return render(request,"crowbar/layouts/splitPage.html",context)
	if request.method == "POST":
		print(request.POST)
		page = getPage(request, request.POST["href"])
		return JsonResponse({"isError":isError,"log":log,"page":page})


@csrf_exempt
def charContent(request, charID=None):
	instance = get_object_or_404(character, id=charID)
	if request.method == "GET":
		context = {"instance":instance.gcaData}
		return render(request,"crowbar/content/simpleChar.html",context)