from django.db import models

def user_directory_path(instance, filename):
    return "camera_{0}/{1}".format(instance.camera.id, filename)


class Camera(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    region = models.CharField(max_length=5)


class Video(models.Model):
    title = models.CharField(max_length=255)
    camera = models.ForeignKey(Camera, on_delete=models.SET_NULL, null=True, blank=True)
    length = models.IntegerField()
    is_processed = models.BooleanField(default=False)
    timecodes = models.JSONField(default=dict, blank=True)
    file = models.FileField(upload_to='static/videos/')