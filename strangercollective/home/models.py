from django.db import models
from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.search import index
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet
from taggit.models import TaggedItemBase, Tag as TaggitTag
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager
from django.utils.safestring import mark_safe
from .blocks import *


def dyn_text(origintext):
	import json
	import re
	text = origintext.replace("</p><p>","</p><br/><p>")
	text = text.replace("<p>","")
	text = text.replace("</p>","")
	text = text.split("<br/>")
	outob = []
	for t in text:
		outtext = ""
		try:
			t = t.replace('&quot;','"')
			t = t.replace('&lt;','<')
			t = t.replace('&gt;','>')
			t = t.replace('\n','<br>')
			jsob = json.loads(t)
			if jsob['type'] == "example":
				text = jsob['text']
				outtext = '<p class="example">%s</p>' % (text) 

		except Exception as e:
			outtext = "<p>%s</p>" % (t)

		outtext = re.sub('^(.+?):','<b>\g<1>:</b>', outtext)
		outtext = re.sub('(p\. [0-9]+?)\)','<a class=pagelink>\g<1></a>)', outtext)
		outob.append(outtext)
	rtext = "".join(outob)
	return rtext

class HomePage(Page):
	body = RichTextField(blank=True)

	content_panels = Page.content_panels + [
		FieldPanel('body', classname="full"),
	]



class BlogIndexPage(Page):
	intro = RichTextField(blank=True)

	content_panels = Page.content_panels + [
		FieldPanel('intro', classname="full")
	]



# Keep the definition of BlogIndexPage, and add:


class BlogPage(Page):
	date = models.DateField("Post date")
	intro = models.CharField(max_length=250)
	body = RichTextField(blank=True)

	search_fields = Page.search_fields + [
		index.SearchField('intro'),
		index.SearchField('body'),
	]

	content_panels = Page.content_panels + [
		FieldPanel('date'),
		FieldPanel('intro'),
		FieldPanel('body', classname="full"),
	]


class GenericIndexPage(Page):
	intro = RichTextField(blank=True)
	content_panels = Page.content_panels + [FieldPanel('intro', classname="full")]

class AdvantageIndexPage(Page):
	intro = RichTextField(blank=True)
	content_panels = Page.content_panels + [FieldPanel('intro', classname="full")]

class DisadvantageIndexPage(Page):
	intro = RichTextField(blank=True)
	content_panels = Page.content_panels + [FieldPanel('intro', classname="full")]

class SkillsIndexPage(Page):
	intro = RichTextField(blank=True)
	content_panels = Page.content_panels + [FieldPanel('intro', classname="full")]

class AdvantagePage(Page):
	body = RichTextField(blank=True)
	points = RichTextField(blank=True)
	special_limitations = RichTextField(blank=True)
	special_enhancements = RichTextField(blank=True)
	feed_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
	exotic = models.BooleanField(default=False)
	physical = models.BooleanField(default=False)
	search_fields = Page.search_fields + [index.SearchField('body'),]
	content_panels = Page.content_panels + [MultiFieldPanel([FieldPanel('exotic'),FieldPanel('physical')], heading="Types", classname="collapsible collapsed"), FieldPanel('points', classname="full"), FieldPanel('body', classname="full"), FieldPanel('special_limitations', classname="full"), FieldPanel('special_enhancements', classname="full"), ]
	promote_panels = [MultiFieldPanel(Page.promote_panels, "Common page configuration"), ImageChooserPanel('feed_image'), ]
	
	@property
	def next_sibling(self):
		return self.get_next_siblings().type(self.__class__).live().first()

	@property
	def prev_sibling(self):
		return self.get_prev_siblings().type(self.__class__).live().first()
	
	@mark_safe
	def body_progress(self):
		return dyn_text(self.body)
	body_progress.allow_tags = True

	@mark_safe
	def limits_dyn(self):
		return dyn_text(self.special_limitations)
	limits_dyn.allow_tags = True

	@mark_safe
	def enhance_dyn(self):
		return dyn_text(self.special_enhancements)
	enhance_dyn.allow_tags = True

	def save(self, *args, **kwargs):
		import re
		s = self.body
		replaced = re.sub('\[(.+?)\]', '<a href="http://localhost:8000/pages/advantages/\g<1>">\g<1></a>', s)
		self.body = replaced
		super(AdvantagePage, self).save(*args, **kwargs)

class DisadvantagePage(Page):
	body = RichTextField(blank=True)
	points = RichTextField(blank=True)
	special_limitations = RichTextField(blank=True)
	special_enhancements = RichTextField(blank=True)
	feed_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
	exotic = models.BooleanField(default=False)
	physical = models.BooleanField(default=False)
	search_fields = Page.search_fields + [index.SearchField('body'),]
	content_panels = Page.content_panels + [MultiFieldPanel([FieldPanel('exotic'),FieldPanel('physical')], heading="Types", classname="collapsible collapsed"), FieldPanel('points', classname="full"), FieldPanel('body', classname="full"), FieldPanel('special_limitations', classname="full"), FieldPanel('special_enhancements', classname="full"), ]
	promote_panels = [MultiFieldPanel(Page.promote_panels, "Common page configuration"), ImageChooserPanel('feed_image'), ]
	
	@property
	def next_sibling(self):
		return self.get_next_siblings().type(self.__class__).live().first()

	@property
	def prev_sibling(self):
		return self.get_prev_siblings().type(self.__class__).live().first()
	
	@mark_safe
	def body_progress(self):
		return dyn_text(self.body)
	body_progress.allow_tags = True

	@mark_safe
	def limits_dyn(self):
		return dyn_text(self.special_limitations)
	limits_dyn.allow_tags = True

	@mark_safe
	def enhance_dyn(self):
		return dyn_text(self.special_enhancements)
	enhance_dyn.allow_tags = True

	def save(self, *args, **kwargs):
		import re
		s = self.body
		replaced = re.sub('\[(.+?)\]', '<a href="http://localhost:8000/pages/advantages/\g<1>">\g<1></a>', s)
		self.body = replaced
		super(DisadvantagePage, self).save(*args, **kwargs)

challenge_choices = (
	('Easy','Easy'),
	('Average','Average'),
	('Hard','Hard'),
	('Very Hard','Very Hard'),
	('Varies','Varies'),
)

class attribute(models.Model):
	attribute_name = models.CharField(max_length=200)
	def __str__(self):
		return self.attribute_name

class SkillsPage(Page):
	feed_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
	body = RichTextField(blank=True)
	attribute = models.ForeignKey('attribute', null=True, blank=True, on_delete=models.SET_NULL, related_name="skills")
	challenge = models.CharField(max_length=200,choices=challenge_choices)
	defaults = RichTextField(blank=True)
	prerequisites = RichTextField(blank=True)


	search_fields = Page.search_fields + [index.SearchField('body'),]
	content_panels = Page.content_panels + [
		MultiFieldPanel([FieldPanel('attribute'),FieldPanel('challenge')], heading="Attribute/Challenge", classname="collapsible collapsed"),
		FieldPanel('defaults', classname="full"),
		FieldPanel('prerequisites', classname="full"),
		FieldPanel('body', classname="full"),
		]
	promote_panels = [MultiFieldPanel(Page.promote_panels, "Common page configuration"), ImageChooserPanel('feed_image'), ]
	
	@property
	def next_sibling(self):
		return self.get_next_siblings().type(self.__class__).live().first()

	@property
	def prev_sibling(self):
		return self.get_prev_siblings().type(self.__class__).live().first()
	
	@mark_safe
	def body_progress(self):
		return dyn_text(self.body)
	body_progress.allow_tags = True

	def save(self, *args, **kwargs):
		super(SkillsPage, self).save(*args, **kwargs)




class PageTag(TaggedItemBase):
    content_object = ParentalKey('DynamicPage', related_name='page_tags')

@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True

class DynamicPage(Page):
	tags = ClusterTaggableManager(through='home.PageTag', blank=True)
	body = StreamField([
		('heading', blocks.CharBlock(classname="full title")),
		('paragraph', blocks.RichTextBlock()),
		('table',TableBlock()),
		('test', TwoColumnBlock()),
		('test2', ColumnBlock()),
		('image', ImageChooserBlock()),
	])
	content_panels = Page.content_panels + [
		StreamFieldPanel('body'),
		FieldPanel('tags'),
	]

