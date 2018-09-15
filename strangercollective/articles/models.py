from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length = 120)
	content = models.TextField()
	updated = models.DateTimeField(auto_now=True,auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	headerimg = models.ImageField(blank=True, null=True)
	tags = TaggableManager()
	def __str__(self):
		return self.title
	def get_absolute_url(self):
		return "/articles/detail/%i/" % self.id