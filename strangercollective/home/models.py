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
from django.db.models.signals import post_save, post_init, post_delete, pre_save
from django.dispatch import receiver
from wagtail.core.models import PageRevision

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
	def get_parents(self, cut="Home"):
		outOb = []
		run = True
		getParent = self
		while run:
			try:
				if getParent.get_parent().title	== cut:
					run = False
				else:
					getParent = getParent.get_parent()
					outOb.append(getParent)
			except:
				run = False
		outOb.reverse()
		return outOb
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

	# def save(self, *args, **kwargs):
	# 	print(":"*40)
	# 	print(self.body)
	# 	import re
	# 	s = self.body
	# 	replaced = re.sub('\[(.+?)\]', '<a href="http://localhost:8000/pages/advantages/\g<1>">\g<1></a>', s)
	# 	self.body = replaced
	# 	super(AdvantagePage, self).save(*args, **kwargs)

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


class SpellsPage(Page):
	feed_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
	body = RichTextField(blank=True)
	challenge = models.CharField(max_length=200,choices=challenge_choices)
	category = models.CharField(max_length=200, null=True, blank=True)
	college = models.CharField(max_length=200, null=True, blank=True)
	duration = models.CharField(max_length=200, null=True, blank=True)
	cost = models.CharField(max_length=200, null=True, blank=True)
	timeToCast = models.CharField(max_length=200, null=True, blank=True)
	prerequisites = models.CharField(max_length=512, null=True, blank=True)


	search_fields = Page.search_fields + [index.SearchField('body'),]
	content_panels = Page.content_panels + [
		# MultiFieldPanel([FieldPanel('challenge')], heading="Attribute/Challenge", classname="collapsible collapsed"),
		FieldPanel('challenge', classname="full"),
		FieldPanel('college', classname="full"),
		FieldPanel('category', classname="full"),
		FieldPanel('duration', classname="full"),
		FieldPanel('cost', classname="full"),
		FieldPanel('timeToCast', classname="full"),
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
		super(SpellsPage, self).save(*args, **kwargs)



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
		('paragraph', dynamicBlock()),
		('table',TableBlock()),
		('test', TwoColumnBlock()),
		('test2', ColumnBlock()),
		('image', ImageChooserBlock()),
	])
	content_panels = Page.content_panels + [
		StreamFieldPanel('body'),
		FieldPanel('tags'),
	]
	renderChildren = models.BooleanField(default=False)
	def get_parents(self, cut="Home"):
		outOb = []
		run = True
		getParent = self
		while run:
			try:
				if getParent.get_parent().title	== cut:
					run = False
				else:
					getParent = getParent.get_parent()
					outOb.append(getParent)
			except:
				run = False
		outOb.reverse()
		return outOb
	def save(self, *args, **kwargs):
		# print(self.body.RawDatavie)
		check = [{"tag":"[/children]","var":"renderChildren", "val":False}]
		for i in self.body:
			# print(dir(i))
			text = str(i.render())
			print("TEXT BLOCK",text,type(text),dir(text))
			for c in check:
				if c["tag"] in text:
					c["val"] = True
		for c in check:
			attrchange = setattr(self, c["var"],c["val"])


		super(DynamicPage, self).save(*args, **kwargs)

	# def clean(self):
	# 	print("Cleaning Dynamic Page")
	def _map(self, outText, soup):
		for p in soup.find_all('p'):
			# print(p.get_text())
			text = p.get_text()
			if text != "":
				outText += '<p>[%s|cat=map]</p>'%(text.title())
		outText = '<div class="map">%s</div>'%(outText)
		return outText

	def serve(self, request, *args, **kwargs):
		from django.template.response import TemplateResponse
		from bs4 import BeautifulSoup
		request.is_preview = getattr(request, 'is_preview', False)
		response = TemplateResponse(
			request,
			self.get_template(request, *args, **kwargs),
			self.get_context(request, *args, **kwargs)
		)
		try:
			print("▼"*40)
			print("Serving Dynamic Page")
			response.render()
			s = response.content.decode("utf-8")

			import re
			from .models import DynamicPage
			from wagtail.core.models import Page
			import json
			# print("cleaning")
			# print(self, dir(self))
			# print(context, dir(context))
			beforeBase = True
			checkBasePage = self
			baseList = ["Campaigns"]
			while beforeBase:
				if checkBasePage.get_parent().title in baseList:
					beforeBase = False
				else:
					checkBasePage = checkBasePage.get_parent()


			pattern = re.compile(r'&lt;.+?&gt;.+?&lt;/.+?&gt;')
			for base in re.findall(pattern,s):
				outText = ""
				match = base.replace("&lt;","<").replace("&gt;",">").replace("></p>",">").replace("<p></","</")
				print(match)
				soup = BeautifulSoup(match, 'html.parser')
				# print(dir(soup.find("function")))
				print(soup.find("function").attrs)
				for k in soup.find("function").attrs:
					functionToRun = getattr(self, "_"+k)
					outText = functionToRun(outText, soup)
				
				s = s.replace(base,outText)

			pattern = re.compile('\[([^/]+?)\]')
			for match in re.findall(pattern,s):
				var = {"cat":"default"}
				lut = {
				"cat_parent":{
				"default": self,
				"character": checkBasePage.get_children().search("Characters")[0].specific,
				"map": checkBasePage.get_children().search("Characters")[0].specific,
				"npc": checkBasePage.get_children().search("Characters")[0].specific,
				}
				}
				# s = value.source
			#     print(match)
				print(match)
				display = match.split("|")[0]
				options = match.split("|")[1:]
				# print(display,options)
				for op in options:
					op = op.replace("=",'":"')
					op = '{"%s"}'%(op)
					op = json.loads(op)
					var.update(op)
				# print(var)
				parent_page = lut["cat_parent"][var["cat"]]
				try:
					# pages = DynamicPage.objects.all().search(display)[0]
					
					pages = parent_page.get_children().search(display)[0]
				except:
					# parent_page = Page.objects.get(title=var["cat"]).specific
					pages = DynamicPage(title=display.title())
					parent_page.add_child(instance=pages)
					pages.save()

					# print("new page",pages)
				# print(type(pages),pages)
				url = pages.url_path.replace("/home/","/pages/")
				replacepattern = '<a href="%s">%s</a>'%(url,display)
				# print(match,replacepattern)
				match = match.replace("|","\|")
				# print(url)
				replaced = re.sub('\[%s\]'%(match), replacepattern, s)
			#     print(replaced)
				s = replaced
			
			pattern = re.compile('\[/.+?\]')
			for match in re.findall(pattern,s):
				print("hide",match)
				s = s.replace(match,'<span style="display:none;">%s</span>'%(match))

			# print(s)
			response.content = s.encode('utf-8')
			print("▲"*40)
			return response
		except Exception as e:
			print("ERROR",e)
			print("▲"*40)
			
			return response


# @receiver(pre_save)
# @receiver(pre_save, sender=PageRevision)
# def preSaveDynamic(sender, instance, *args, **kwargs):
	# try:
	# 	print("▼"*40)
	# 	import re
		
	# 	# print(dir(instance))
	# 	# print(instance.page, type(instance.page))
	# 	s = instance.body
	# 	pages = DynamicPage.objects.all().search("Rat")
	# 	print("pages", pages)
	# 	replaced = re.sub('\[(.+?)\]', '<a href="http://localhost:8000/pages/advantages/\g<1>">\g<1></a>', s)
	# 	replaced = "<p>Hello</p>"
	# 	instance.body = replaced
	# 	print(replaced)
	# 	print("done",sender,instance)
	# 	# instance.save()
	# except Exception as e:
	# 	try:
			
	# 		print("error",e)
	# 	except:
	# 		pass
	# 	pass
	# print("▲"*40)
@receiver(post_save, sender=PageRevision)
def postSaveDynamic(sender, instance, *args, **kwargs):
	instance.publish()
	pass