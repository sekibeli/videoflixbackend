import uuid
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets

from user.models import CustomUser
from videoflixbackend.serializers import CustomUserSerializer
from videoflixbackend.models import Video
from .serializers import ResetPasswordSerializer

from django.core.cache import cache
from random import randint


class SignupView(APIView):    
    permission_classes = []
    authentication_classes = []


    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if CustomUser.objects.filter(email=request.data["email"]).exists():
            return Response({"error": "An error occured"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.is_valid(raise_exception=True)    
        user = CustomUser(**serializer.data)
        password = request.data.get('password')
        user.set_password(password)
        user.save()
        self.send_verification_email(user) #Try except einbauen?

        return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)
    

    def send_verification_email(self, user):
        subject = 'Please confirm your email'
        context = {
            'username': user.username,
            'verification_url': f'{settings.FRONTEND_URL}/verify/{user.verification_token}'
        }
        
        html_content = render_to_string('email_verification.html', context)
        text_content = render_to_string('email_verification.txt', context)

        email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()



class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def get(self, request, token, format=None):
        try:
            user = CustomUser.objects.get(verification_token=token)
            user.is_verified = True
            user.save()
            return Response({"message": "E-Mail successfully verified."}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "Invaild Token"}, status=status.HTTP_400_BAD_REQUEST)
        
 
class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if not user.is_verified:
                return Response({"error": "Please verify your email first."}, status=status.HTTP_401_UNAUTHORIZED)

            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid login data"}, status=status.HTTP_401_UNAUTHORIZED)        
      

class GuestLoginView(APIView):
    def post(self, request):
        random_number = randint(1000, 9999)
        guest_username = f'guest_{random_number}'

        guest_user = CustomUser.objects.create_user(
            username=guest_username, 
            password=uuid.uuid4().hex,
            is_guest=True)
        token, created = Token.objects.get_or_create(user=guest_user)

        return Response({
            "token": token.key,
            "user_id": guest_user.pk,
            "username": guest_user.username,
            "email": guest_user.email
        })
    

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)   
      

class LoggeduserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)   
    
    def patch(self, request):
        serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        try:
            user.delete()
            return Response({"message": "User account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"error": "User account deletion failed"}, status=status.HTTP_400_BAD_REQUEST)



class UserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return CustomUser.objects.all()  
        return CustomUser.objects.none() 


class ToggleLike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, videoId):
        user = request.user
        video = get_object_or_404(Video, pk=videoId)

        if user in video.likes.all():
            video.likes.remove(user)
            liked = False
        else:
            video.likes.add(user)
            liked = True

        cache.delete('video_list_cache_key')

        return Response({'liked': liked}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                user = CustomUser.objects.get(email=data['email'])
                if default_token_generator.check_token(user, data['token']):
                    user.set_password(data['password'])
                    user.save()
                    return Response({'message': 'Successfully reset password.'})
                return Response({'error': 'Invalid Token.'}, status=status.HTTP_400_BAD_REQUEST)
            except CustomUser.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)