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
        read_only_fields = ['is_processed',]

class TimecodeAddSerializer(serializers.Serializer):
    video = serializers.IntegerField
    timecodes = serializers.JSONField

class UploadVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['file',]

class TimecodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['timecodes']

    def to_representation(self, instance):
        return instance.timecodes if instance.timecodes else None