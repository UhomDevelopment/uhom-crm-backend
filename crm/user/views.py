from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.views import APIView

from user.serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer


class RegisterView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=serializer.context).data,
            "token": AuthToken.objects.create(user)[1]
        })

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=serializer.context).data,
            "token": AuthToken.objects.create(user)[1]
        })

class AddSuperUserView(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            'username': 'admin',
            'password': 'admin',
            'is_staff': True
        }
        serializer = CreateUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        return Response({
            "user": {'username': 'admin',
            'password': 'admin'},
            "token": AuthToken.objects.create(user)[1]
        })

