from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

# Create your models here.
class collection(models.Model):
	collection_name = models.CharField(max_length=255, unique=True)
	def __str__(self):
		return self.collection_name

class panorama(models.Model):
	collection = models.ForeignKey(collection, on_delete=models.CASCADE, related_name='panorama')
	panorama_name = models.CharField(max_length=255, unique=True)
	image = models.ImageField()
	stereoscopic = models.BooleanField(default=False)
	cubemap = models.BooleanField(default=False)
	extraimage = models.ImageField(blank=True)
	
	PX = models.ImageField(blank=True)
	PY = models.ImageField(blank=True)
	PZ = models.ImageField(blank=True)
	NX = models.ImageField(blank=True)
	NY = models.ImageField(blank=True)
	NZ = models.ImageField(blank=True)

	def loopurl(self):
		return r"%s/%s" %(self.collection.collection_name, self.panorama_name)

	def save(self):
		if self.cubemap and not self.stereoscopic:
			#Opening the uploaded image
			im = Image.open(self.image)
			w, h = im.size
			print(w,h)

			#Resize/modify the image
			ims = {
			"PX": {"x0":0,"x1":(w/6)*1,"y0":0,"y1":h},
			"PY": {"x0":(w/6)*1,"x1":(w/6)*2,"y0":0,"y1":h},
			"PZ": {"x0":(w/6)*2,"x1":(w/6)*3,"y0":0,"y1":h},
			"NX": {"x0":(w/6)*3,"x1":(w/6)*4,"y0":0,"y1":h},
			"NY": {"x0":(w/6)*4,"x1":(w/6)*5,"y0":0,"y1":h},
			"NZ": {"x0":(w/6)*5,"x1":(w/6)*6,"y0":0,"y1":h},
			}
			# output = BytesIO()
			# self.image = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
			for k,v in ims.items():
				output = BytesIO()
				print(k)
				print(v)
				temp = im.crop((v["x0"], v["y0"], v["x1"], v["y1"]))
				temp.save(output, format='JPEG', quality=100)
				output.seek(0)
				setattr(self, k, InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None))

			super(panorama,self).save()

		if self.stereoscopic and not self.cubemap:
			#Opening the uploaded image
			im = Image.open(self.image)
			w, h = im.size
			loutput = BytesIO()

			#Resize/modify the image
			lim = im.crop((0, 0, w, h/2))

			#after modifications, save it to the loutput
			lim.save(loutput, format='JPEG', quality=100)
			loutput.seek(0)
			

			routput = BytesIO()
			rim = im.crop((0, h/2, w, h))
			rim.save(routput, format='JPEG', quality=100)
			routput.seek(0)

			#change the imagefield value to be the newley modifed image value
			self.image = InMemoryUploadedFile(loutput,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(loutput), None)
			self.extraimage = InMemoryUploadedFile(routput,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(routput), None)

			super(panorama,self).save()
		if not self.stereoscopic and not self.cubemap:
			#Opening the uploaded image
			im = Image.open(self.image)
			w, h = im.size
			loutput = BytesIO()

			#Resize/modify the image
			lim = im.crop((0, 0, w, h))

			#after modifications, save it to the loutput
			lim.save(loutput, format='JPEG', quality=100)
			loutput.seek(0)
			

			routput = BytesIO()
			rim = im.crop((0, 0, w, h))
			rim.save(routput, format='JPEG', quality=100)
			routput.seek(0)

			#change the imagefield value to be the newley modifed image value
			self.image = InMemoryUploadedFile(loutput,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(loutput), None)
			self.extraimage = InMemoryUploadedFile(routput,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(routput), None)
			super(panorama,self).save()