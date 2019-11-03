from django.contrib import admin

# Register your models here.
from .models import *

class ListAdmin(admin.ModelAdmin):
	pass

class testresultAdmind(admin.ModelAdmin):
	list_display = ("test", "identifier", "question", "notes", "date", "score", "ip", "pcusername",)
	list_filter = ("test",)
	search_fields = ["identifier","pcusername","ip",]

admin.site.register(profile, ListAdmin)
admin.site.register(submission, ListAdmin)
admin.site.register(testresult, testresultAdmind)