from django.contrib import admin
from .models import *

# Register your models here.
class ListAdmin(admin.ModelAdmin):
	pass

admin.site.register(AdvantagePage, ListAdmin)
admin.site.register(TestPage, ListAdmin)
