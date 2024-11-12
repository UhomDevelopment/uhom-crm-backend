from django.db import models

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=255)
    cam_id = models.IntegerField()
    length = models.IntegerField()