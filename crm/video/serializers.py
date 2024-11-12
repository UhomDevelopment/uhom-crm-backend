from rest_framework import serializers

from video.models import Camera, Video


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class TimecodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['timecodes']