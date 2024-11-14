from django.urls import path
from rest_framework.serializers import ListSerializer

from app import settings
from video.views import AddCameraView, RetrieveUpdateDestroyCameraView, ListCameraView, RetrieveUpdateDestroyVideoView, \
    ListVideoView, AddVideoView, ListCameraTimecodesView

urlpatterns = [
    path('camera/add/', AddCameraView.as_view(), name='add'),
    path('camera/<int:pk>', RetrieveUpdateDestroyCameraView.as_view()),
    path('cameras', ListCameraView.as_view()),
    path('video/<int:pk>', RetrieveUpdateDestroyVideoView.as_view()),
    path('video/add', AddVideoView.as_view()),
    path('videos/<int:cam_pk>', ListVideoView.as_view()),
    path('videos/', ListVideoView.as_view()),
    path('timecodes/<int:pk>', ListCameraTimecodesView.as_view()),
]