from django.urls import path
from rest_framework.serializers import ListSerializer

from user.views import RegisterView, LoginView
from video.views import AddCameraView, RetrieveUpdateDestroyCameraView, ListCameraView, RetrieveDestroyView, \
    ListVideoView, AddVideoView, ListCameraTimecodesView

urlpatterns = [
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', LoginView.as_view()),
]
