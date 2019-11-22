from django.contrib import admin
from .models import *
# Register your models here.

class mapAdmin(admin.ModelAdmin):
	readonly_fields = ("splitImage",)

admin.site.register(map,mapAdmin)
