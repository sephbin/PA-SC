from django.contrib import admin
from .models import *
# Register your models here.

class mapAdmin(admin.ModelAdmin):
	pass


admin.site.register(map,mapAdmin)
