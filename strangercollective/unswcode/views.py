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

def start_test(request, testid, idi, password):
	log = []
	try:
		testOb = get_object_or_404(test, testName = testid)
		log.append("/testOb")
		if testOb.enabled and testOb.testPassword == password:
			log.append("/if")
			nutestStart, created = testStart.objects.update_or_create(
				test = testOb,
				identifier = idi,
				)
			log.append("/up_or_create")
			return JsonResponse({"start":True,"message":"Test started, you have until %s to finish"%(str(nutestStart.endTime))})
		else:
			return JsonResponse({"start":False,"message":"Test is either not enabled or the password is incorrect"})

	except Exception as e:
		return JsonResponse({"start":False, "log":log,"message":str(e)})


def get_test_question(request, question):
	try:
		tq = get_object_or_404(testquestion, questionName = question)
		outob = {
		"questionName"	:	tq.questionName,
		"questionText"	:	tq.questionText,
		"questionHint"	:	tq.questionHint,
		"archjson"		:	tq.archjson(),
		}
		return JsonResponse(outob)
	except:
		return JsonResponse({})



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
	"score": 2,
	}
	log = []
	if request.method == "POST":
		try:
			data = request.POST["data"]
			r = json.loads(data)
			created = True	
			try:
				obj = testresult(**r).save()
			except:
				created = False

			return JsonResponse({"created":created})
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			other = sys.exc_info()[0].__name__
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			errorType = str(exc_type)
			return JsonResponse({"isError": True, "error":str(e), "errorType":errorType, "function":fname, "line":exc_tb.tb_lineno, "log":log})
	else:
		return JsonResponse(jsob)
def marklist(request, testName):
	import collections
	# testOb = get_object_or_404(test, testName= testName)
	trOb = testresult.objects.filter(test=testName)
	aR  = {}
	fullScore = 0
	questionSet = []

	for tr in trOb:
		# print(tr.question)
		questionSet.append(tr.question)

	questionSet = list(set(questionSet))
	questionSet.sort()
	fullScore = len(questionSet)
	
	for tr in trOb:
		try:
			aR[tr.identifier]
		except:
			aR[tr.identifier] = {}
			questionDict = collections.OrderedDict()
			for k in questionSet:
				questionDict[k] = {"obs":[],"score":0}
			aR[tr.identifier]['questions'] = questionDict

		aR[tr.identifier]['questions'][tr.question]["obs"].append(tr)
		aR[tr.identifier]['pc']=tr.pcusername
		if tr.score > 0:
			print(tr.identifier,tr.question,tr.score)
			aR[tr.identifier]['questions'][tr.question]["score"] = int(tr.score)

	for st, marks in aR.items():
		marks['total'] = 0
		for q, data in marks['questions'].items():
			marks['total'] += data['score']
		marks['percent'] = round(marks['total']/fullScore*100,2)
	context = {
	"marks":aR,
	}
	print(context)
	return render(request, "code/testresults.html",context)





def changemarks(request):
	import datetime
	import pytz
	log = []
	try:
		utc=pytz.UTC
		cutoff = utc.localize(datetime.datetime(2019,11,5, 7))
		# tres = testresult.objects.filter(notes__icontains="CORRECT!"
		tres = testresult.objects.filter(question="3-05")
			# , pcusername="Nimat"
			# )
		# tres = [tres[0]]
		for tr in tres:
			notes = tr.notes
			notes = float(notes.split(" ")[-1])
			if notes < 160:
				tr.score = 1
				tr.save()
			# log.append([tr.date, tr.question])
			# if tr.date < cutoff:
				# log.append([tr.notes,tr.date])
				# tr.score = 2
				# tr.save()
			# if tr.notes == "CORRECT! Correct quantity of lines Model accuracy is correct":
				# tr.score = 1

		return JsonResponse({"log":log})
	except Exception as e:
		return JsonResponse({"log":log, "error":str(e)})
