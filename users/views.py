from django.shortcuts import render
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from users.models import User, ConsumerProfile, Bank
from users.serializers import (
    RegisterSerializer,
    EmailVerificationSerializer,
    LoginSerializer,
    ConsumerProfileSerializer,
    BankSerializer
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from users.utils import Util
import jwt
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsUser
# Create your views here.



class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_url = reverse('email-verify')
        absolute_url = f"http://{current_site}{relative_url}?token={str(token)}"

        email_body = f"Hi {user.username} use this link to verify your email\nLink: {absolute_url}"

        email_data = {
            'email_subject': "Verification email",
            'email_body': email_body,
            'to_email': user.email
        }

        Util.send_email(email_data)

        return Response({"data": serializer.data, "mssg": "user created"}, status=status.HTTP_201_CREATED)


class VerifyEmailAPIView(APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({"email": "Succesfully verified"}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({"error": "Activation link expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({"error": "Token is invalid, couldn't decode"}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PrepareConsumerProfile(RetrieveUpdateAPIView):
    serializer_class = ConsumerProfileSerializer
    queryset = ConsumerProfile.objects.all()
    permission_classes = (IsUser, ) 
    lookup_field = "id" 

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
