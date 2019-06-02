from django.contrib import admin
from .models import *

# Register your models here.
class ListAdmin(admin.ModelAdmin):
	pass

admin.site.register(AdvantagePage, ListAdmin)
admin.site.register(DisadvantagePage, ListAdmin)
admin.site.register(DynamicPage, ListAdmin)
admin.site.register(attribute)