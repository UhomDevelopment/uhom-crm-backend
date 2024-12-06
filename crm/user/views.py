from http.client import responses

from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiExample, OpenApiParameter
from rest_framework import permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from knox.models import AuthToken
from rest_framework.views import APIView

from user.serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer, CreateSuperUserSerializer, \
    ReasonResponseSerializer, ResponseLoginUserSerializer


@extend_schema_view(
    post=extend_schema(
        summary="Регистрация",
        responses={
            200: ResponseLoginUserSerializer,
            400: ReasonResponseSerializer
        }
    ),
)
class RegisterView(APIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=serializer.context).data,
            "token": AuthToken.objects.create(user)[1]
        })


@extend_schema_view(
    post=extend_schema(
        summary="Авторизация",
        responses={
            200: ResponseLoginUserSerializer,
            400: ReasonResponseSerializer
        },
    ),
)


class LoginView(APIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=serializer.context).data,
            "token": AuthToken.objects.create(user)[1]
        })

@extend_schema_view(
    get=extend_schema(
        summary="Получить суперпользователя",
        description='Тестовый пользователь для регистрации других аккаунтов',
        responses={
            201: CreateSuperUserSerializer
        }
    ),
)
class AddSuperUserView(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            'username': 'admin',
            'password': 'admin',
            'is_staff': True
        }

        serializer = CreateUserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
        else:
            user = User.objects.get(username='admin')

        data['token'] = AuthToken.objects.create(user)[1]

        response_serializer = CreateSuperUserSerializer(data=data)
        response_serializer.is_valid(raise_exception=True)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

