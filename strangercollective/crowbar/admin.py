from django.contrib import admin
from .models import *
import sys
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text

m_list_display = ['enabled','enableDelete','pk','name','hasError','updated','data',]
m_list_editable = ['enabled', 'enableDelete',]
m_list_display_links = ['name',]
m_list_filter = ['enabled','enableDelete']
m_search_fields = ["name","data",]
m_readonly_fields = ['css', 'data',]
m_actions = ['resaveSelected','enableDeleteSelected', 'disableDeleteSelected',]
m_save_on_top = True
m_save_as = True

# Register your models here.
class master(admin.ModelAdmin):
	list_display = m_list_display
	list_editable = m_list_editable
	list_display_links = m_list_display_links
	search_fields = m_search_fields
	readonly_fields = m_readonly_fields
	list_filter = m_list_filter
	actions = m_actions
	save_on_top = m_save_on_top
	save_as = m_save_as

	def resaveSelected(self, request, queryset):
		queryset.update()
	resaveSelected.short_description = "Resave Selected"
	def enableDeleteSelected(self, request, queryset):
		queryset.update(enableDelete=True)
	enableDeleteSelected.short_description = "Enable Delete Selected"
	def disableDeleteSelected(self, request, queryset):
		queryset.update(enableDelete=False)
	disableDeleteSelected.short_description = "Disable Delete Selected"

class feature_relative_inline(admin.TabularInline):
	model = feature_relative
	readonly_fields = ('obClass',)
	autocomplete_fields = ("feature",)
	fields = (
		'feature',
		'obClass',
		'rank',
		
		)
	extra = 0
class choice_inline(admin.TabularInline):
	model = choice
	# readonly_fields = ('obClass',)
	readonly_fields = ("get_edit_link", )
	# autocomplete_fields = ("feature",)
	fields = (
		'choiceType',
		"get_edit_link",
		)
	extra = 0
	def get_edit_link(self, obj=None):
		if obj.pk:  # if object has already been saved and has a primary key, show link to it
			url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)])
			return mark_safe("""<a href="{url}&_popup=1">{text}</a>""".format(
				url=url,
				text=_("Edit this %s separately") % obj._meta.verbose_name,
			))
		return _("(save and continue editing to create a link)")
	get_edit_link.short_description = _("Edit link")
	get_edit_link.allow_tags = True
class choice_admin(master):
	inlines = (feature_relative_inline,)

class characterTemplate_admin(master):
	inlines = (feature_relative_inline, choice_inline)

for subclass in parentModel.__subclasses__():
	try:
		adminOb = getattr(sys.modules[__name__], str(subclass.__name__)+"_admin")
	except Exception as e:
		adminOb = master
	admin.site.register(subclass, adminOb)