from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import *

def index(request, path=None):
	import requests
	import markdown
	import re, glob, os
	from git import Repo

	mediaPath = settings.MEDIA_ROOT
	subpath = os.path.join(mediaPath,"mimir","1")
	try:	Repo.clone_from("https://github.com/sephbin/SyCoDe_Scribe", subpath)
	except Exception as e: print(e)
	md_files = glob.glob(subpath + "\**\*.md", recursive = True)
	searchFile = "The Sublime Run of the Tangerine Oroborus.md"
	if path:
		searchFile = path
	md_files = list(filter(lambda x:x.endswith(searchFile), md_files))
	with open(md_files[0],"r") as file:
		mdtext = file.read()
	
	# \[{2}(.+?)\]{2}
	search = re.finditer(r"\[{2}(.+?)\]{2}", mdtext)
	for s in search:
		print(s)
		print(s.group(1))
		fromString = s.group(1)
		try:	toString = fromString.split("|")[1]
		except:	toString = fromString.split("|")[0]
		# toString = fromString.replace("[[","[").replace("]]","]")
		toLink = fromString.split("|")[0]
		fromString = "[[%s]]"%(fromString)
		toString = "[%s]"%(toString)
		toLink = "(%s.md)"%(toLink)
		mdtext = mdtext.replace(fromString,toString+toLink)
	mdtext = mdtext.replace("\n","\n\n")
	html = markdown.markdown(mdtext)

	# https://sephbin.github.io/SyCoDe_Scribe/
	# https://raw.githubusercontent.com/sephbin/SyCoDe_Scribe/main/README.md
	return HttpResponse(html)
