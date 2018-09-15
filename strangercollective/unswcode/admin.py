from django.contrib import admin

# Register your models here.
from .models import *

class ListAdmin(admin.ModelAdmin):
	pass

admin.site.register(profile, ListAdmin)
admin.site.register(submission, ListAdmin)