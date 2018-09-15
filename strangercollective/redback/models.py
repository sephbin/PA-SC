from django.db import models

# Create your models here.

class rb_item(models.Model):
	archiJson = models.TextField(max_length = 99999)
	displayGeom = models.TextField(max_length = 99999, blank=True, null=True)
	def __str__(self):
		return str(self.id)