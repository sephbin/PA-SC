import datetime
from django.db import models
from django.utils import timezone, html
import django.utils.html as dhtml
from colorfield.fields import ColorField
from taggit.managers import TaggableManager
import uuid
from markdownx.models import MarkdownxField


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class project(models.Model):
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return (self.number+" - "+self.name)

class category(models.Model):
    name = models.CharField(max_length=200)
    colour = ColorField(default='#FFFFFF')
    def __str__(self):
        return self.name

class finishCode(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, unique=True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

class supplier(models.Model):
    company =models.CharField(max_length=200)
    representative=models.CharField(max_length=200)
    phone=models.CharField(max_length=20, blank=True, null=True)
    email=models.EmailField(blank=True, null=True)
    def __str__(self):
        return (self.company +": "+self.representative)

class finish(models.Model):
    code = models.ForeignKey(finishCode, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)
    fin_product = models.CharField(max_length=200, blank=True, null=True)
    fin_finish =models.CharField(max_length=200, blank=True, null=True)
    fin_colour =models.CharField(max_length=200, blank=True, null=True)
    fin_code =models.CharField(max_length=200, blank=True, null=True)
    fin_size = models.CharField(max_length=200, blank=True, null=True)
    fin_notes = models.CharField(max_length=200, blank=True, null=True)
    supplier = models.ForeignKey(supplier, on_delete=models.CASCADE, null=True)

    def image_tag(self):
        return dhtml.mark_safe('<img src="/media/%s" width="150" height="auto" />' % (self.image))
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def finish(self):
        return dhtml.mark_safe('<div><b>Product: </b>%s<br><b>Finish: </b>%s<br><b>Colour: </b>%s<br><b>Code: </b>%s<br><b>Size: </b>%s<br><b>Notes: </b>%s<br></div>' % (self.fin_product, self.fin_finish, self.fin_colour, self.fin_code, self.fin_size, self.fin_notes))
    def supplytext(self):
        return dhtml.mark_safe('<div><b>Company: </b>%s<br><b>Rep: </b>%s<br><b>Ph: </b><a href="tel:%s">%s</a><br><b>Email: </b><a href="mailto:%s">%s</a><br></div>' % (self.supplier.company, self.supplier.representative, self.supplier.phone, self.supplier.phone, self.supplier.email,self.supplier.email))
    supplytext.short_description = 'Supplier'
    def __str__(self):
        try:
            findetails = [self.fin_product,self.fin_finish,self.fin_colour]
            findettext = " - ".join(findetails)
            return (str(self.code)+": "+findettext)
        except:
            return "BROKEN"

class door_leafType(models.Model):
    code = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class door_frameType(models.Model):
    code = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class door(models.Model):
    leafType = models.ForeignKey(door_leafType, on_delete=models.CASCADE, null=True)
    frameType = models.ForeignKey(door_frameType, on_delete=models.CASCADE, null=True)
    leafFinish = models.ForeignKey(finish, on_delete=models.CASCADE, null=True, related_name='leafFinish')
    frameFinish = models.ForeignKey(finish, on_delete=models.CASCADE, null=True, related_name='frameFinish')
    def __str__(self):
        return "DOOR"

class room(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    json = models.CharField(max_length=200, blank=True)
    area = models.FloatField()
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    file = models.CharField(max_length=200)
    zone = models.CharField(max_length=200)
    project = models.ForeignKey(project, on_delete=models.CASCADE)
    tags = TaggableManager()

    doors = models.ManyToManyField(door, through='rel_roomDoor',through_fields=('room', 'door'), blank=True,)
    myfield = MarkdownxField()
    def __str__(self):
        return self.name

class rel_roomDoor(models.Model):
    room = models.ForeignKey(room, on_delete=models.CASCADE)
    door = models.ForeignKey(door, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def leafFinish(self):
        return self.door.leafFinish
    def frameFinish(self):
        return self.door.frameFinish
    def leafType(self):
        return self.door.leafType
    def frameType(self):
        return self.door.frameType
    def leafFinishTag(self):
        return self.door.leafFinish.image_tag()
    def frameFinishTag(self):
        return self.door.frameFinish.image_tag()
    def code(self):
            return ("DR"+str(self.id))




