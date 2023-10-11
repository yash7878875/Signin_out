import datetime
from rest_framework import generics, status
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.contrib.auth import authenticate
from django.utils import timezone
from signin_out.settings import SECRET_KEY
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.authentication import TokenAuthentication

class RegisterAPI(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                validated_data = serializer.validated_data

                username = validated_data.get("username", None)
                first_name = validated_data.get("first_name", None)
                last_name = validated_data.get("last_name", None)
                date_of_birth = validated_data.get("date_of_birth", None)
                password = validated_data.get("password", None)
                email = validated_data.get("email", None)
                country = validated_data.get("country", None)
                profile_image = request.FILES.get('profile_image')

                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        "username": username,
                        "first_name": first_name,
                        "last_name": last_name,
                        "date_of_birth": date_of_birth,
                        "password": make_password(password),
                        "country": country,

                    }
                )

                if profile_image:
                    user.profile_image = profile_image

                otp = get_random_string(length=6, allowed_chars='1234567890')
                subject = 'OTP'
                email_from = settings.EMAIL_HOST_USER
                email_to = [email]
                send_mail(subject, otp, email_from, email_to)

                if otp:
                    user.otp = otp
                    user.save()

                return Response({"status": True, 'message': "Registered successfully and sent OTP email in varify"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"status": False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class verify_otp(generics.GenericAPIView):

    def post(self, request):
        data = request.data
        print(data)
        email = data["email"]
        otp_entered = data["otp"]
        email_otp = User.objects.get(email=email)
        print(email_otp, "*"*100)
        if email_otp.otp == otp_entered:
            email_otp.is_verified = True
            email_otp.is_active = True
            email_otp.save()

            return Response('OTP verified. You are now logged in.')

        else:
            return Response('Invalid OTP. Please try again.')


class LoginView(generics.GenericAPIView):

    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):

        data = request.data
        email = data.get("email", "")
        password = data.get("password", "")
        if not email:
            return Response({"status": False, 'message': "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response({"status": False, 'message': "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        if user:

            serializer_class = self.get_serializer(data=request.data)
            if serializer_class.is_valid(raise_exception=True):
                if not user.is_verified:
                    return Response({"status": False, 'message': "Please Verify Your Account"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    user_data = {"user_id": user.id,
                                 "email": user.email, "tokens": user.tokens}
                    user.last_login = timezone.now()
                    user.save()
                    return Response({"status": True, 'message': "valid_credentials", 'data': user_data}, status=status.HTTP_200_OK)

        return Response({'message': "Invalid Email and password"}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({
            "status": True,
            "message": "Successfully.",
        }, status=status.HTTP_200_OK)
    

class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({ "message": "Successfully."},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({ "message": "Token valid."},status=status.HTTP_400_BAD_REQUEST)

