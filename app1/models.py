from django.db import models

# Create your models here.
class Document(models.Model):
	title = models.CharField(max_length=50,default='null')
	author = models.CharField(max_length=50, default='null') #clientid of the person who uploaded the file
	description = models.CharField(max_length=500, blank=True)
	accesslevel = models.CharField(max_length=50, default=4)
	document = models.FileField(upload_to='documents/')
	uploaded_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title
class DetectorUpload(models.Model):
	document = models.FileField(upload_to='detector/')
	clientid = models.CharField(max_length=50, default='null')
	username = models.CharField(max_length=50, default='null')
	designation = models.CharField(max_length=50, default='null')
	m = models.CharField(max_length=150, default='null') #retrieved from image
	mdash = models.CharField(max_length=150, default='null') #calculated from clientID
	status = models.CharField(max_length=20, default='Not Viewed') #culprit detected or not
	uploaded_at = models.DateTimeField(auto_now_add=True)
