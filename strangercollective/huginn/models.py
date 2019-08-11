from django.db import models

# Create your models here.
class family(models.Model):
	name = models.CharField(max_length = 120)
	gh_script = models.TextField(max_length = 9999, default ="print('no script')")
	def __str__(self):
		return self.name