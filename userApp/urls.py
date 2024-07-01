from django.urls import path

from userApp.apps import UserappConfig
from userApp.views import RegistrationAPIView, VerifyCodeAPIView, ProfileAPIView

app_name = UserappConfig.name

urlpatterns = [
    path('create/', RegistrationAPIView.as_view(), name='user-create'),
    path('verify/', VerifyCodeAPIView.as_view(), name='user-verify'),
    path('profile/', ProfileAPIView.as_view(), name='user-profile'),
]
