from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index
from wagtail.images.edit_handlers import ImageChooserPanel


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


class AdvantageIndexPage(Page):
	intro = RichTextField(blank=True)

	content_panels = Page.content_panels + [
		FieldPanel('intro', classname="full")
	]

class AdvantagePage(Page):
	body = RichTextField(blank=True)
	special_limitations = RichTextField(blank=True)
	special_enhancements = RichTextField(blank=True)
	feed_image = models.ForeignKey(
		'wagtailimages.Image',
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='+'
	)
	exotic = models.BooleanField(default=False)
	physical = models.BooleanField(default=False)



	search_fields = Page.search_fields + [
		index.SearchField('body'),
	]

	content_panels = Page.content_panels + [
	MultiFieldPanel([FieldPanel('exotic'),FieldPanel('physical')], heading="Types", classname="collapsible collapsed"),
	FieldPanel('body', classname="full"),
	FieldPanel('special_limitations', classname="full"),
	FieldPanel('special_enhancements', classname="full"),
	]

	promote_panels = [
		MultiFieldPanel(Page.promote_panels, "Common page configuration"),
		ImageChooserPanel('feed_image'),
	]