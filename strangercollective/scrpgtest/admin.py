from django.contrib import admin
# Register your models here.
from .models import *

class modInline(admin.StackedInline):
	model = modifier
	# fields = ('name','description','modifier')
	extra = 0 # how many rows to show

class advInline(admin.TabularInline):
	model = rel_advantage
	readonly_fields = ('cost','mods',)
	fields = ('advantage','rank','cost','modifiers','mods')
	extra = 0 # how many rows to show
class disadvInline(admin.TabularInline):
	model = rel_disadvantage
	readonly_fields = ('cost','mods',)
	fields = ('disadvantage','rank','cost','modifiers','mods')
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

class characterModelAdmin(admin.ModelAdmin):
	list_display = ("__str__","cost","status")
#   list_display_links = ["updated"]
	list_filter = ["race","status"]
	search_fields = ["name"]
	list_editable = ["status"]
	readonly_fields = ('cost',)
	# fields = ('cost',)
	inlines = (advInline, disadvInline, skillInline, languageInline)
admin.site.register(character, characterModelAdmin)

class modPackageAdmin(admin.ModelAdmin):
	inlines = (modInline,)
	# pass

class listAdmin(admin.ModelAdmin):
	pass

class advantageAdmin(admin.ModelAdmin):
	list_display = ("__str__","basecost")
admin.site.register(campaign,listAdmin)
admin.site.register(characterType,listAdmin)
admin.site.register(race,listAdmin)
admin.site.register(status,listAdmin)
admin.site.register(rel_advantage,listAdmin)
admin.site.register(advantage,advantageAdmin)
admin.site.register(disadvantage,advantageAdmin)
admin.site.register(modifier,listAdmin)
admin.site.register(skill,listAdmin)
admin.site.register(language,listAdmin)
admin.site.register(specialmodifier,listAdmin)
admin.site.register(modPackage,modPackageAdmin)
