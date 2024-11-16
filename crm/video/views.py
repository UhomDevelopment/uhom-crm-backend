from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from video.models import Camera, Video
from video.serializers import CameraSerializer, VideoSerializer, TimecodeSerializer

import os
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser

from django.conf import settings
from rest_framework import status
from .models import Video
from .serializers import VideoSerializer


class AddCameraView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

class RetrieveUpdateDestroyCameraView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

class ListCameraView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

class RetrieveUpdateDestroyVideoView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

class ListVideoView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get_queryset(self):
        if camera_pk := self.kwargs.get('cam_pk', None):
            camera = Camera.objects.get(pk=camera_pk)
            return Video.objects.filter(camera=camera)
        else:
            return Video.objects.all()

class ListCameraTimecodesView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Camera.objects.all()
    serializer_class = TimecodeSerializer

    def get_queryset(self):
        videos = Video.objects.filter(camera_id=self.kwargs.get('pk', None))
        return videos

class AddVideoView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        upload_id = request.data.get('uploadId')
        chunk_index = int(request.data.get('chunkIndex', 0))
        total_chunks = int(request.data.get('totalChunks', 1))
        video_title = request.data.get('title')
        camera_id = request.data.get('camera_id')  
        length = request.data.get('length')
        video_file = request.data.get('file')

        if not upload_id or not video_file:
            raise ValidationError("Missing required parameters: uploadId or file.")

        
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_uploads', upload_id)
        os.makedirs(temp_dir, exist_ok=True)
        temp_chunk_path = os.path.join(temp_dir, f'chunk_{chunk_index}')

        
        with open(temp_chunk_path, 'wb') as temp_file:
            temp_file.write(video_file.read())

        
        if len(os.listdir(temp_dir)) == total_chunks:
            
            final_file_name = f"{upload_id}.mp4"
            final_file_path = os.path.join(settings.MEDIA_ROOT, 'static/videos', final_file_name)
            os.makedirs(os.path.dirname(final_file_path), exist_ok=True)

            with open(final_file_path, 'wb') as final_file:
                for i in range(total_chunks):
                    chunk_path = os.path.join(temp_dir, f'chunk_{i}')
                    with open(chunk_path, 'rb') as chunk_file:
                        final_file.write(chunk_file.read())

            
            for chunk in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, chunk))
            os.rmdir(temp_dir)

            
            video = Video.objects.create(
                title=video_title,
                camera_id=camera_id,
                length=length,
                file=f'static/videos/{final_file_name}'
            )
            serializer = self.serializer_class(video)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'message': 'Chunk uploaded', 'chunkIndex': chunk_index})



