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
	maxZoom = models.IntegerField(default=0)

	def __str__(self):
		return str(self.map_name)

	def splitImage(self):
		log=[]
		#Opening the uploaded image
		delim = "/"
		if os.name == 'nt':
			delim = "\\"
		print("delim",delim)
		im = Image.open(self.image)
		w, h = im.size
		print("wh:",w,h)


		fullRes = w
		if h > w: fullRes = h
		maxdiv = math.ceil(fullRes/256)
		print("maxdiv:",maxdiv)
		maxzoom = 0
		dyndiv = 1
		while dyndiv*2 < maxdiv:
			dyndiv = 2 ** maxzoom
			maxzoom += 1
		# maxzoom += 0
		print("maxzoom:",maxzoom)
		self.maxZoom = maxzoom
		zooms = list(range(maxzoom+1))
		basepath = settings.MEDIA_ROOT+"maps"
		# basepath = basepath.replace("/","")
		mapPath = basepath+"\\%s"%(self.map_name)
		print("mappath",mapPath)
		try:					os.makedirs(mapPath.replace("\\",delim))
		except Exception as e:	log.append(str(e))
		for z in zooms:
			revzooms = zooms[::-1]
			scale = revzooms[zooms.index(z)]
			# scale += 0
			print("Scale",scale)
			zpath = mapPath+"\\%s"%(str(z))
			zpath = zpath.replace("\\",delim)
			try:					os.mkdir(zpath)
			except Exception as e:	log.append(str(e))
			ylist = list(range(2**z))
			print(ylist)
			for y in ylist:
				tilepath = zpath+"\\%s"%(str(y))
				try:					os.mkdir(tilepath.replace("\\",delim))
				except Exception as e:	log.append(str(e))
				xlist = list(range(2**z))
				for x in xlist:
					zscale = 2**scale
					print("zscale", zscale)
					nw = math.ceil(w/zscale)
					nh = math.ceil(h/zscale)
					x0, x1 = (x*265)+x, ((x+1)*265)+x
					y0, y1 = (y*265)+y, ((y+1)*265)+y
					if x0 <= nw and y0 <= nh:
						scaled_image =  im.resize((nw,nh), Image.ANTIALIAS)
						path = tilepath+"\\%s.png" %(str(x))
						temp = scaled_image.crop((x0, y0, x1, y1)) #x0 y0 x1 y1
						temp.save(path.replace("\\",delim), format='PNG', quality=100)
		return log

	def save(self):
		self.splitImage()

		super(map,self).save()

	class Meta:
		ordering = ['map_name']