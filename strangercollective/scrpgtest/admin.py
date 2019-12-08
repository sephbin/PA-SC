from django.contrib import admin
# Register your models here.
from .models import *

# class modInline(admin.StackedInline):
	# model = modifier
	# fields = ('name','description','modifier')
	# extra = 0 # how many rows to show

class advInline(admin.TabularInline):
	model = rel_advantage
	readonly_fields = ('cost',
		# 'mods',
		)
	fields = ('advantage','rank','cost',
		# 'modifiers','mods'
		)
	extra = 0 # how many rows to show
class disadvInline(admin.TabularInline):
	model = rel_disadvantage
	readonly_fields = ('cost',
		# 'mods',
		)
	fields = ('disadvantage','	rank','cost',
		# 'modifiers','mods'
		)
	extra = 0 # how many rows to 
class skillInline(admin.TabularInline):
	model = rel_skill
	readonly_fields = ('skill_challenge','skill_attribute','relative_skill','relative_value','cost')
	fields = ('skill','skill_challenge','skill_attribute','rank','relative_skill','relative_value','cost')
	extra = 0 # how many rows to show
class languageInline(admin.TabularInline):
	model = rel_language
	readonly_fields = ('cost',)
	fields = ('language','written','spoken','cost')
	extra = 0 # how many rows to show

class possessionInline(admin.TabularInline):
	model = rel_possession
	readonly_fields = ('cost',)
	fields = ('ammount','possession','cost')
	extra = 1 # how many rows to show

class characterModelAdmin(admin.ModelAdmin):
	list_display = ("__str__","id","cost","status")
#   list_display_links = ["updated"]
	list_filter = ["race","status"]
	search_fields = ["name"]
	list_editable = ["status"]
	readonly_fields = ('cost',)
	# fields = ('cost',)
	inlines = (advInline, disadvInline, skillInline, languageInline, possessionInline)
admin.site.register(character, characterModelAdmin)

class possessionModelAdmin(admin.ModelAdmin):
	filter_horizontal = ('campaign','possession_category',) 

class skillModelAdmin(admin.ModelAdmin):
	filter_horizontal = ('campaign',) 


class modPackageAdmin(admin.ModelAdmin):
	# inlines = (modInline,)
	pass

class listAdmin(admin.ModelAdmin):
	pass

class advantageAdmin(admin.ModelAdmin):
	list_display = ("__str__","basecost")

class mapAdmin(admin.ModelAdmin):
	# fields = ('map_name', 'campaign', 'image', 'maxZoom')
	pass


admin.site.register(map,mapAdmin)
admin.site.register(campaign,listAdmin)
admin.site.register(characterType,listAdmin)
admin.site.register(race,listAdmin)
admin.site.register(status,listAdmin)
admin.site.register(rel_advantage,listAdmin)
admin.site.register(advantage,advantageAdmin)
admin.site.register(disadvantage,advantageAdmin)
admin.site.register(modifier,listAdmin)
admin.site.register(skill,skillModelAdmin)
admin.site.register(language,listAdmin)
admin.site.register(possession,possessionModelAdmin)
admin.site.register(specialmodifier,listAdmin)
admin.site.register(modPackage,modPackageAdmin)
admin.site.register(rel_possession,listAdmin)
admin.site.register(possession_category)
admin.site.register(rel_skill)
admin.site.register(mapLayer)
