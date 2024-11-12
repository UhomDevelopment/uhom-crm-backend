from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveDestroyAPIView

from video.models import Camera, Video
from video.serializers import CameraSerializer, VideoSerializer, TimecodeSerializer


class AddCameraView(CreateAPIView):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

class RetrieveUpdateDestroyCameraView(RetrieveUpdateDestroyAPIView):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

class ListCameraView(ListAPIView):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

class AddVideoView(CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class RetrieveDestroyView(RetrieveDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

class ListVideoView(ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get_queryset(self):
        if camera_pk := self.kwargs.get('cam_pk', None):
            camera = Camera.objects.get(pk=camera_pk)
            return Video.objects.filter(camera=camera)
        else:
            return Video.objects.all()

class ListCameraTimecodesView(ListAPIView):
    queryset = Camera.objects.all()
    serializer_class = TimecodeSerializer

    def get_queryset(self):
        videos = Video.objects.filter(camera_id=self.kwargs.get('pk', None))
        return videos
