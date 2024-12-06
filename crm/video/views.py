from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiExample
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from user.serializers import ReasonResponseSerializer
from video.models import Camera, Video
from video.serializers import CameraSerializer, VideoSerializer, TimecodeSerializer, UploadVideoSerializer, \
    TimecodeAddSerializer

import os
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser

from django.conf import settings
from rest_framework import status
from .models import Video
from .serializers import VideoSerializer

@extend_schema_view(
    post=extend_schema(
        summary="Создать камеру",
        responses={
            200: CameraSerializer,
            400: ReasonResponseSerializer,
            401: ReasonResponseSerializer,
        }
    ),
)
class AddCameraView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

@extend_schema_view(
    get=extend_schema(
        summary="Получить информацию о камере",
        responses={
            200: CameraSerializer,
            400: ReasonResponseSerializer,
            401: ReasonResponseSerializer,
        }
    ),
    put=extend_schema(
        summary="Изменить информацию о камере целиком",
        responses={
            200: CameraSerializer,
            400: ReasonResponseSerializer,
            401: ReasonResponseSerializer,
        }
    ),
    patch=extend_schema(
        summary="Изменить часть информации о камере",
        responses={
            200: CameraSerializer,
            400: ReasonResponseSerializer,
            401: ReasonResponseSerializer,
        }
    ),
    delete=extend_schema(
        summary="Удалить камеру",
        responses={
            200: CameraSerializer,
            400: ReasonResponseSerializer,
            401: ReasonResponseSerializer,
        }
    )
)
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

@extend_schema_view(
    get=extend_schema(
        summary="Список таймкодов",
        examples=[
            OpenApiExample(
                'Пример',
                value=
                    [
                      [
                        0.06666666666666667,
                        15.6
                      ],
                      [
                        98.33333333333333,
                        195.4
                      ],
                      [
                        721.6,
                        732.8
                      ],
                    ]
            )
        ]
    )
)
class ListCameraTimecodesView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Camera.objects.all()
    serializer_class = TimecodeSerializer

    def get_queryset(self):
        videos = Video.objects.filter(camera_id=self.kwargs.get('pk', None))
        return videos

@extend_schema_view(
    post=extend_schema(
        summary="Добавить видео",
        description="Добавить информацию о видео если файл уже был загружен",
    ),
)
class AddVideoInfoView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

@extend_schema_view(
    post=extend_schema(
        summary="Добавить таймкоды",
        description="Добавить таймкоды в видео если уже было загружен",
        responses={
            200: VideoSerializer,
            400: ReasonResponseSerializer,
        }
    ),
)
class AddTimecodesView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TimecodeAddSerializer

    def post(self, request):
        video_id = request.data.get('video', None)
        timecodes = request.data.get('timecodes')

        video = Video.objects.get(pk=video_id)
        video.timecodes = timecodes
        video.save()
        return Response(VideoSerializer(video).data)




# class UploadVideoView(CreateAPIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = Video.objects.all()
#     serializer_class = UploadVideoSerializer
#     parser_classes = [MultiPartParser]
#
#     def post(self, request, *args, **kwargs):
#         upload_id = request.data.get('uploadId')
#         chunk_index = int(request.data.get('chunkIndex', 0))
#         total_chunks = int(request.data.get('totalChunks', 1))
#         video_title = request.data.get('title')
#         camera_id = request.data.get('camera_id')
#         length = request.data.get('length')
#         video_file = request.data.get('file')
#
#         if not upload_id or not video_file:
#             raise ValidationError("Missing required parameters: uploadId or file.")
#
#
#         temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_uploads', upload_id)
#         os.makedirs(temp_dir, exist_ok=True)
#         temp_chunk_path = os.path.join(temp_dir, f'chunk_{chunk_index}')
#
#
#         with open(temp_chunk_path, 'wb') as temp_file:
#             temp_file.write(video_file.read())
#
#
#         if len(os.listdir(temp_dir)) == total_chunks:
#
#             final_file_name = f"{upload_id}.mp4"
#             final_file_path = os.path.join(settings.MEDIA_ROOT, 'static/videos', final_file_name)
#             os.makedirs(os.path.dirname(final_file_path), exist_ok=True)
#
#             with open(final_file_path, 'wb') as final_file:
#                 for i in range(total_chunks):
#                     chunk_path = os.path.join(temp_dir, f'chunk_{i}')
#                     with open(chunk_path, 'rb') as chunk_file:
#                         final_file.write(chunk_file.read())
#
#
#             for chunk in os.listdir(temp_dir):
#                 os.remove(os.path.join(temp_dir, chunk))
#             os.rmdir(temp_dir)
#
#
#             video = Video.objects.create(
#                 title=video_title,
#                 camera_id=camera_id,
#                 length=length,
#                 file=f'static/videos/{final_file_name}'
#             )
#             serializer = self.serializer_class(video)
#
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response({'message': 'Chunk uploaded', 'chunkIndex': chunk_index})

class GetHoursFromCamera(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        videos = Video.objects.filter(camera_id=self.kwargs.get('pk', None))
        data = TimecodeSerializer(videos, many=True).data
        seconds = 0

        for timecodes_list in data[0]:
            seconds += timecodes_list[1] - timecodes_list[0]
        return Response(int(seconds/3600))
