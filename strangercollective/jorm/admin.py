from django.contrib import admin
from .models import *
# Register your models here.

class item_objectInline(admin.TabularInline):
    model = item_object.throughs.through
    fk_name = 'object_from'
    extra = 0 # how many rows to show

class item_objectAdmin(admin.ModelAdmin):
	model = item_object
	readonly_fields = ('data',)
	fields = ('name','json_text','data',)
	inlines = [item_objectInline,]

class through_objectAdmin(admin.ModelAdmin):
	model = through_object


admin.site.register(item_object,item_objectAdmin)
admin.site.register(through_object,through_objectAdmin)