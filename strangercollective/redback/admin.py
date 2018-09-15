from django.contrib import admin

# Register your models here.
from .models import *

class listAdmin(admin.ModelAdmin):
	pass

admin.site.register(rb_item, listAdmin)