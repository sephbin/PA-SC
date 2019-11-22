from django.contrib import admin
from .models import *
# Register your models here.

class mapAdmin(admin.ModelAdmin):
	fields = ('map_name', 'image', 'maxZoom')

admin.site.register(map,mapAdmin)
