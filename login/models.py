from django.db import models

# Create your models here.
class LoginDetails(models.Model):
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	designation = models.IntegerField(default=1)
	clientid = models.CharField(max_length=17, default="xyz")
	cipher_text = models.CharField(max_length=25, default="xyz")
	hash_text = models.CharField(max_length=65, default="xyz")

	def __str__(self):
		return self.username