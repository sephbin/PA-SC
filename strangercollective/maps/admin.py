from django.contrib import admin
from .models import *
# Register your models here.

class mapAdmin(admin.ModelAdmin):
	readonly_fields = ("splitImage",)
	fields = ('map_name', 'image', 'maxZoom', 'splitImage',)

admin.site.register(map,mapAdmin)
