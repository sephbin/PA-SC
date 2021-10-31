from wagtail.admin.edit_handlers import (FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel)
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class dynamicBlock(blocks.RichTextBlock):

    # def clean(self, value):
    #     try:
    #         import re
    #         from .models import DynamicPage
    #         from wagtail.core.models import Page
    #         import json
    #         print("▼"*40)
    #         print("cleaning")
    #         s = value.source
    #         pattern = re.compile('\[(.+?)\]')
    #         for match in re.findall(pattern,s):
    #             var = {"cat":"Cleanup"}
    #             s = value.source
    #             print(match)
    #             display = match.split("|")[0]
    #             options = match.split("|")[1:]
    #             print(display,options)
    #             for op in options:
    #                 op = op.replace("=",'":"')
    #                 op = '{"%s"}'%(op)
    #                 op = json.loads(op)
    #                 var.update(op)
    #             print(var)
    #             try:
    #                 pages = DynamicPage.objects.all().search(display)[0]
    #             except:
    #                 parent_page = Page.objects.get(title=var["cat"]).specific
    #                 pages = DynamicPage(title=display.title())
    #                 parent_page.add_child(instance=pages)
    #                 pages.save()

    #                 print("new page",pages)
    #             print(type(pages),pages)
    #             url = pages.url_path.replace("/home/","/pages/")
    #             replacepattern = '<a href="%s">%s</a>'%(url,display)
    #             print(match,replacepattern)
    #             match = match.replace("|","\|")
    #             print(url)
    #             replaced = re.sub('\[%s\]'%(match), replacepattern, s)
    #             print(replaced)
    #             value.source = replaced
    #         return value
    #     except Exception as e:
    #         print(e)
    #         return value
    #     print("▲"*40)
    
    def render_basic(self, value, context=None):
        try:
            # import re
            # from .models import DynamicPage
            # from wagtail.core.models import Page
            # import json
            print("▼"*40)
            # print("cleaning")
            # s = value.source
            # print(self, dir(self))
            # print(context, dir(context))
            # pattern = re.compile('\[(.+?)\]')
            # for match in re.findall(pattern,s):
            #     var = {"cat":"Cleanup"}
            #     s = value.source
            #     print(match)
            #     display = match.split("|")[0]
            #     options = match.split("|")[1:]
            #     print(display,options)
            #     for op in options:
            #         op = op.replace("=",'":"')
            #         op = '{"%s"}'%(op)
            #         op = json.loads(op)
            #         var.update(op)
            #     print(var)
            #     try:
            #         pages = DynamicPage.objects.all().search(display)[0]
            #     except:
            #         parent_page = Page.objects.get(title=var["cat"]).specific
            #         pages = DynamicPage(title=display.title())
            #         parent_page.add_child(instance=pages)
            #         pages.save()

            #         print("new page",pages)
            #     print(type(pages),pages)
            #     url = pages.url_path.replace("/home/","/pages/")
            #     replacepattern = '<a href="%s">%s</a>'%(url,display)
            #     print(match,replacepattern)
            #     match = match.replace("|","\|")
            #     print(url)
            #     replaced = re.sub('\[%s\]'%(match), replacepattern, s)
            #     print(replaced)
            #     value.source = replaced
            print("▲"*40)
            return value
        except Exception as e:
            print(e)
            print("▲"*40)
            return value
class ColumnBlock(blocks.StreamBlock):
    heading = blocks.CharBlock(classname="full title")
    paragraph = dynamicBlock()
    image = ImageChooserBlock()

    class Meta:
        template = 'home/blocks/column.html'

class TwoColumnBlock(blocks.StructBlock):

    left_column = ColumnBlock(icon='arrow-right', label='Left column content')
    right_column = ColumnBlock(icon='arrow-right', label='Right column content')

    class Meta:
        template = 'home/blocks/two_column_block.html'
        icon = 'placeholder'

    # def clean(self, value):
    #     import re
    #     print("▼"*40)
    #     print("cleaning")
    #     print(type(value), value)
    #     print(dir(value))
    #     for v in value.items():
    #         t = v[1]
    #         s = t.rawtext
    #         replaced = re.sub('\[(.+?)\]', '<a href="http://localhost:8000/pages/advantages/\g<1>">\g<1></a>', s)
    #         # print(type(s),s)
    #         # print(dir(s))
    #         t.rawtext = replaced
    #         # v.replace("e","3")
    #     print("▲"*40)
    #     return(value)