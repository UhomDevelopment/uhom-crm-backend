from django.urls import path
from rest_framework.serializers import ListSerializer

from user.views import RegisterView, LoginView, AddSuperUserView

urlpatterns = [
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('auth/addadmin/', AddSuperUserView.as_view())
]
