from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import *

def index(request, path=None):
	log = []
	try:
		import requests
		import markdown
		import re, glob, os, json
		import git

		mediaPath = settings.MEDIA_ROOT
		subpath = os.path.join(mediaPath,"mimir","1")
		try:	git.Repo.clone_from("https://github.com/sephbin/SyCoDe_Scribe", subpath)
		except Exception as e:
			log.append(str(e))
			try:
				repo = git.Repo(subpath)
				o = repo.remotes.origin
				o.pull()
			except Exception as e:
				print(e)
				log.append(str(e))
		globPath = os.path.join(subpath,"**","*.md")
		md_files = glob.glob(globPath, recursive = True)
		log.append(subpath)
		log.append(md_files)
		searchFile = "README.md"
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
		html = html+"<br>"+json.dumps(logobj)

		# https://sephbin.github.io/SyCoDe_Scribe/
		# https://raw.githubusercontent.com/sephbin/SyCoDe_Scribe/main/README.md
		return HttpResponse(html)
	except Exception as e:
		return JsonResponse({"log":log, "error":str(e)})