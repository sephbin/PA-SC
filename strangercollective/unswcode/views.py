from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
# from .forms import PostForm
from .models import *
from django.contrib  import messages
from django.contrib.auth.decorators import login_required, user_passes_test

import json, sys, os
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
	subs1 = submission.objects.filter(user=request.user, assignment="19CODE1240AS1")
	subs2 = submission.objects.filter(user=request.user, assignment="19CODE1240AS2")
	subs3 = submission.objects.filter(user=request.user, assignment="19CODE1240AS3")
	context = {
	"author":"Andrew Butler",
	"user":request.user,
	"AS1":subs1.last(),
	"AS2":subs2.last(),
	"AS3":subs3.last(),
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

def viewmark(request, ass_id):
	sub = get_object_or_404(submission, id=ass_id)
	return HttpResponse(sub.mark)	

@user_passes_test(teacher_check)
def marking(request, ass_no):
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
						# try:	total += 100*int(m)
						# except: pass
				postData[s]["total"] =  total
				sub.mark = json.dumps(postData[s])
				sub.save()
			except Exception as e:
				stringOb += str(e)
		return HttpResponse(stringOb)
	subs = submission.objects.filter(assignment=ass_no)
	cleansubs = {}
	cleanlist = []
	for s in subs:
		cleansubs[s.user] = s
	for k in cleansubs:
		cleanlist.append(cleansubs[k])
	for c in cleanlist:
		try:
			c.mark = json.loads(c.mark)
		except:
			c.mark = {}
	context = {"subs":cleanlist}
	return render(request, ass_no+".html", context)


@csrf_exempt
def submit_test_question(request):
	'''
	test = models.CharField(max_length=256)
	identifier = models.CharField(max_length=256)
	question = models.TextField(max_length=256)
	notes = models.TextField(max_length=1000)
	date = models.DateTimeField(auto_now=True)
	score = models.IntegerField(default=0)
	'''
	
	jsob = {
	"test": "Grasshopper Test v0.8",
	"identifier": "Example",
	"question": "Challenge 01",
	"notes": "CORRECT",
	"score": 1,
	}
	log = []
	if request.method == "POST":
		try:
			data = request.POST["data"]
			r = json.loads(data)
			try:
				obj = testresult(**r).save()


			return JsonResponse({"created":created})
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			other = sys.exc_info()[0].__name__
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			errorType = str(exc_type)
			return JsonResponse({"isError": True, "error":str(e), "errorType":errorType, "function":fname, "line":exc_tb.tb_lineno, "log":log})
	else:
		return JsonResponse(jsob)