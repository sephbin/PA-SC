from django.contrib import admin
from .models import *
from markdownx.admin import MarkdownxModelAdmin

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class doorsInline(admin.TabularInline):
    model = rel_roomDoor
    readonly_fields = ('code','frameType','frameFinish','leafType','leafFinish','leafFinishTag','frameFinishTag',)
    fields = ('code','door','quantity','frameType','frameFinish','frameFinishTag','leafType','leafFinish','leafFinishTag',)
    extra = 0 # how many rows to show


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_filter = ['pub_date']
    search_fields = ['question_text']
admin.site.register(Question, QuestionAdmin)
class finishAdmin(admin.ModelAdmin):
    list_filter = ['code','supplier']
    list_display = ('code','finish','image_tag','supplytext')
    fieldsets = [
        (None,               {'fields': ['code','image','image_tag',]}),
        ('Finish', {'fields': ['fin_product','fin_finish','fin_colour','fin_code','fin_size','fin_notes',], 'classes': ['collapse']}),
        ('Supplier', {'fields': ['supplier',], 'classes': ['collapse']}),
    ]
    readonly_fields = ('image_tag',)

admin.site.register(finish,finishAdmin)
class listAdmin(admin.ModelAdmin):
    pass
class rel_roomDoorAdmin(admin.ModelAdmin):
    list_display = ('room','door','quantity','code')
    pass
admin.site.register(door, listAdmin)
admin.site.register(door_frameType, listAdmin)
admin.site.register(door_leafType, listAdmin)
admin.site.register(rel_roomDoor, rel_roomDoorAdmin)
admin.site.register(supplier)

admin.site.register(finishCode, listAdmin)

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'area', 'file', 'tag_list')
    search_fields = ['name']
    list_filter = ['category','tags']
    inlines = (doorsInline,)
    def get_queryset(self, request):
        return super(RoomAdmin, self).get_queryset(request).prefetch_related('tags')
    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
# admin.site.register(room, RoomAdmin)
admin.site.register(room, MarkdownxModelAdmin)


class projectAdmin(admin.ModelAdmin):
    list_display = ('number', 'name')
admin.site.register(project, projectAdmin)

class categoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'colour')
admin.site.register(category, categoryAdmin)

