from django.contrib import admin
from .models import *

class parameterOb_Admin(admin.ModelAdmin):
	# readonly_fields = ('mapTree',)
	# fields = ('name','json_text','data',)
	# inlines = [item_objectInline,]
	model = parameterOb

# Register your models here.
admin.site.register(family)
admin.site.register(functionOb)
admin.site.register(parameterOb, parameterOb_Admin)
admin.site.register(parameterMapThrough)