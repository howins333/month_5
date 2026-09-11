from .serializers import UserRegisterSerializer
from .models import UserConfirmation
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random


class RegistrationAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = User.objects.create_user(
            username=username,
            password=password,
            is_active=False
        )

        code = str(random.randint(100000, 999999))

        UserConfirmation.objects.create(
            user=user,
            code=code
        )

        return Response(
            {
                'user_id': user.id,
                'code': code
            },
            status=status.HTTP_201_CREATED
        )


class AuthorizationAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:
            token, created = Token.objects.get_or_create(
                user=user
            )

            return Response({
                'token': token.key
            })

        return Response(
            {'detail': 'Неверный логин или пароль'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class ConfirmUserAPIView(CreateAPIView):

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        code = request.data.get('code')

        try:
            confirmation = UserConfirmation.objects.get(
                user_id=user_id
            )
        except UserConfirmation.DoesNotExist:
            return Response(
                {'detail': 'Код подтверждения не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        if confirmation.code != code:
            return Response(
                {'detail': 'Неверный код'},
                status=status.HTTP_400_BAD_REQUEST
            )

        confirmation.user.is_active = True
        confirmation.user.save()

        confirmation.delete()

        return Response(
            {'detail': 'Пользователь успешно подтвержден'},
            status=status.HTTP_200_OK
        )