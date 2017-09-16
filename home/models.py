from django.db import models

# Create your models here.
class Crowdedness(models.Model):
    nameStr = models.CharField(primary_key = True, max_length=100)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    when = models.DateTimeField(auto_now_add=True)
    lat = models.CharField(max_length=100)
    lng = models.CharField(max_length=100)
    crowdedness = models.IntegerField()

class Wifi(models.Model):
	when = models.DateTimeField(auto_now_add=True, verbose_name=b'timestamp')
	mag = models.IntegerField()

class Noise(models.Model):
	when = models.DateTimeField(auto_now_add=True, verbose_name=b'timestamp')
	mag = models.IntegerField()
