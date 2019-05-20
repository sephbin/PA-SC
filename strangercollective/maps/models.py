from django.db import models
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.safestring import mark_safe
from django.conf import settings

from PIL import Image
import math
from io import BytesIO
import sys, os

class map(models.Model):
	map_name = models.CharField(max_length=255, unique=True)
	image = models.ImageField()
	tfirst = models.ImageField(blank=True)

	def __str__(self):
		return str(self.map_name)

	def save(self):
		#Opening the uploaded image
		im = Image.open(self.image)
		w, h = im.size
		print(w,h)


		fullRes = w
		if h > w: fullRes = h
		maxdiv = math.ceil(fullRes/256)
		print(maxdiv)
		maxzoom = 0
		dyndiv = 1
		while dyndiv*2 < maxdiv:
			dyndiv = 2 ** maxzoom
			maxzoom += 1
		print(maxzoom)
		zooms = list(range(maxzoom+1))
		basepath = settings.MEDIA_ROOT+"\\maps"
		basepath = basepath.replace("/","")
		mapPath = basepath+"\\%s"%(self.map_name)
		try:					os.mkdir(mapPath)
		except Exception as e:	print(e)
		for z in zooms:
			revzooms = zooms[::-1]
			scale = revzooms[zooms.index(z)]
			zpath = mapPath+"\\%s"%(str(z))
			try:					os.mkdir(zpath)
			except Exception as e:	print(e)
			ylist = list(range(2**z))
			print(ylist)
			for y in ylist:
				tilepath = zpath+"\\%s"%(str(y))
				try:					  os.mkdir(tilepath)
				except Exception as e:	print(e)
				xlist = list(range(2**z))
				for x in xlist:
					pass
					# print("!!!!----------------------------!!!!")
					nw = math.ceil(w/(2**scale))
					nh = math.ceil(h/(2**scale))
					scaled_image =  im.resize((nw,nh), Image.ANTIALIAS)
					path = tilepath+"\\%s.png" %(str(x))
					x0, x1 = (x*265)+x, ((x+1)*265)+x
					y0, y1 = (y*265)+y, ((y+1)*265)+y
					temp = scaled_image.crop((x0, y0, x1, y1)) #x0 y0 x1 y1
					temp.save(path, format='PNG', quality=100)
		# output.seek(0)
		# setattr(self, 'tfirst', InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None))

		super(map,self).save()

	class Meta:
		ordering = ['map_name']