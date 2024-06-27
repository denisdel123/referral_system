import time

from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from userApp.models import User
from userApp.serializers import RegisterSerializer, VerifyCodeSerializer, ProfileActivatedInviteSerializer, \
    ProfileInputInviteSerializer
from userApp.services import generate_invite_code, generate_verification_code
from userApp.tasks import send_test_code


class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        phone_number = serializer.validated_data["phone_number"]

        user, create = User.objects.get_or_create(phone_number=phone_number)

        if create:
            user.set_password(None)  # Устанавливаем пустой пароль, если пользователь новый
            user.invite_code = generate_invite_code()  # Генерация инвайт-кода
            user.save()
        time.sleep(2)
        code = generate_verification_code()
        send_test_code.delay(phone_number, code)
        user.verification_code = "1234"
        user.save()

        return Response({"detail": "Код верификации отправлен"}, status=status.HTTP_200_OK)


class VerifyCodeAPIView(generics.GenericAPIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        code = serializer.validated_data["code"]
        user = get_object_or_404(User, phone_number=phone_number, verification_code=code)
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        },
            status=status.HTTP_200_OK
        )


class ProfileAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.user.activated_invite_code:
            return ProfileActivatedInviteSerializer
        else:
            return ProfileInputInviteSerializer
