from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
# from .forms import PostForm
from .models import *
from django.contrib  import messages
from django.contrib.auth.decorators import login_required, user_passes_test
import json
# Create your views here.

def teacher_check(user):
	groups = user.groups.all()
	groups = list(map(lambda x: x.name, groups))
	test = "UNSW_TEACHER" in groups
	return test

def post_delete(request):

	return HttpResponse("<h1>Delete</h1>")



def lecture(request,lecture_wk):
	context = {
	"author":"Andrew Butler"
	}
	return render(request, "lecture_wk"+str(lecture_wk)+".html",context)

def lecture2(request):
	context = {
	"author":"Andrew Butler"
	}
	return render(request, "lecture_wk2.html",context)

@login_required(login_url="/sc/login/")
def codeHome(request):
	subs = submission.objects.filter(user=request.user, assignment="CODE1240 AS1")
	context = {
	"author":"Andrew Butler",
	"user":request.user,
	"AS1":subs.last(),
	}
	return render(request, "codeHome.html",context)

def submit(request, ass_no):
	context={
	"assignment":ass_no,
	"user":request.user,
	}
	return render(request, "codeSubmit.html", context)

def submitPost(request):
	if request.method == "POST":
		sub = submission(user=request.user, link=request.POST['link'], assignment=request.POST['assignment'])
		sub.save()
		return HttpResponseRedirect("/code/")

@user_passes_test(teacher_check)
def marking(request):
	if request.method == "POST":
		postData = json.loads(request.POST["data"])
		stringOb = ""
		for s in postData:
			stringOb = s
			try:
				sub = submission.objects.get(id=s)
				stringOb = sub.link
				total = 0
				for m in postData[s]:
					try:
						total += float(postData[s][m]['val'])*float(postData[s][m]['weight'])
					except:
						pass
				postData[s]["total"] =  total
				sub.mark = json.dumps(postData[s])
				sub.save()
			except Exception as e:
				stringOb += str(e)
		return HttpResponse(stringOb)
	subs = submission.objects.filter(assignment="CODE1240 AS1")
	cleansubs = {}
	cleanlist = []
	for s in subs:
		cleansubs[s.user] = s
	for k in cleansubs:
		cleanlist.append(cleansubs[k])
	for c in cleanlist:
		c.mark = json.loads(c.mark)
	context = {"subs":cleanlist}
	return render(request, "codeMarking.html", context)
