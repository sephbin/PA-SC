from django.contrib import admin

# Register your models here.
from .models import *

class ListAdmin(admin.ModelAdmin):
	pass

class testresultAdmind(admin.ModelAdmin):
	list_display = ("test", "identifier", "question", "notes", "date", "score", "ip", "pcusername",)
	list_filter = ("test","identifier",)
	search_fields = ["identifier","pcusername","ip",'notes','question',]

class testQuestionAdmin(admin.ModelAdmin):
	list_display = ("questionName", "questionText", "questionHint", "_archjson",)
	list_editable = ("_archjson",)

admin.site.register(profile, ListAdmin)
admin.site.register(submission, ListAdmin)
admin.site.register(testresult, testresultAdmind)
admin.site.register(testquestion, testQuestionAdmin)
admin.site.register(test)
admin.site.register(testStart)