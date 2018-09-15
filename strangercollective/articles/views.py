from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .forms import PostForm
from .models import Post
from django.contrib  import messages
# Create your views here.

def post_create(request):
	form = PostForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		messages.error(request, "Failed Creation")
	context = {
	"form":form,
	}
	return render(request, "article_form.html",context)

def post_detail(request, article_id):
	instance = get_object_or_404(Post, id=article_id)
	queryset = Post.objects.all()
	queryset = queryset[::-1]
	queryset.remove(instance)
	queryset = queryset[:3]
	context = {"title":instance.title,
	"instance": instance,
	"object_list": queryset,
	"user":request.user
	}

	return render(request, "article_detail.html",context)

def post_list(request):
	queryset = Post.objects.all()
	queryset = queryset[::-1]
	# if request.user.is_authenticated:
	context = {"title":"List",
	"object_list": queryset,
	"user":request.user
	}
	return render(request, "index.html",context)

def post_update(request, article_id=None):
	instance = get_object_or_404(Post, id=article_id)
	form = PostForm(request.POST or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Successfully Saved")
		return HttpResponseRedirect(instance.get_absolute_url())
	queryset = Post.objects.all()
	queryset = queryset[::-1]
	queryset.remove(instance)
	queryset = queryset[:3]
	context = {"title":instance.title,
	"instance": instance,
	"object_list": queryset,
	"user":request.user,
	"form":form,
	}

	return render(request, "article_form.html",context)

def post_delete(request):

	return HttpResponse("<h1>Delete</h1>")