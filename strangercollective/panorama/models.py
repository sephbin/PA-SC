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
	extraimage = models.ImageField(blank=True)
	
	def loopurl(self):
		return r"%s/%s" %(self.collection.collection_name, self.panorama_name)

	def save(self):
		if self.stereoscopic:
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
		else:
			super(panorama,self).save()