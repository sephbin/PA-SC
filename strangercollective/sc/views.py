from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
# Create your views here.

def signup_view(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			# log the user in
			login(request,user)
			if 'next' in request.POST:
				return HttpResponseRedirect(request.POST.get("next"))
			else:
				return HttpResponseRedirect("/")
	else:
		form = UserCreationForm()
	context = {"form":form}
	return render(request, "accounts/signup.html", context)

def login_view(request):
	if request.method == "POST":
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			#log in the user
			user = form.get_user()
			login(request,user)
			if 'next' in request.POST:
				return HttpResponseRedirect(request.POST.get("next"))
			else:
				return HttpResponseRedirect("/")
	else:
		form = AuthenticationForm()
	context = {'form':form}
	return render(request,"accounts/login.html",context)

def logout_view(request):
	if request.method == "POST":
		logout(request)
		return HttpResponseRedirect("/")

def updatewebsite(request):
	import subprocess
	subprocess.call('/home/sephbin/PA-SC/strangercollective/auto.sh')
	return HttpResponse("UPDATED")