from django.urls import path

from video.views import AddCameraView, RetrieveUpdateDestroyCameraView, ListCameraView, RetrieveUpdateDestroyVideoView, \
    ListVideoView, ListCameraTimecodesView, VideoUploadView

urlpatterns = [
    path('camera/add/', AddCameraView.as_view(), name='add'),
    path('camera/<int:pk>', RetrieveUpdateDestroyCameraView.as_view()),
    path('cameras', ListCameraView.as_view()),
    path('video/<int:pk>', RetrieveUpdateDestroyVideoView.as_view()),
    path('video/upload', VideoUploadView.as_view()),
    path('videos/<int:cam_pk>', ListVideoView.as_view()),
    path('videos/', ListVideoView.as_view()),
    path('timecodes/<int:pk>', ListCameraTimecodesView.as_view()),
]