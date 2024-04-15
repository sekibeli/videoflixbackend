from rest_framework import serializers
from django.conf import settings
from user.models import CustomUser
from django.contrib.auth.password_validation import validate_password
from .models import Video, VideoQuality

class VideoSerializer(serializers.ModelSerializer):
    video_url = serializers.SerializerMethodField('get_video_url')

    class Meta:
        model = Video
        fields = '__all__'  
        extra_kwargs = {'likes': {'required': False}}

    def get_video_url(self, obj):
        request = self.context.get('request')
        video_url = obj.video_file.url if obj.video_file else ''
        if request is not None:
            return request.build_absolute_uri(video_url)
        return video_url 
    

class VideoQualitySerializer(serializers.ModelSerializer):
    video_file_url = serializers.SerializerMethodField('get_video_file_url')

    class Meta:
        model = VideoQuality
        fields = ('quality', 'video_file', 'video_file_url')

    def get_video_file_url(self, obj):
        request = self.context.get('request')
        video_file_url = obj.video_file.url if hasattr(obj.video_file, 'url') else ''
        print("Request:", request)  # Debug-Ausgabe
        print("URL vor build_absolute_uri:", video_file_url)  # Debug-Ausgabe
        if request is not None:
            return request.build_absolute_uri(video_file_url)
        return video_file_url

    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'is_verified']

        extra_kwargs = {
            'password': {'write_only': True},
            'is_verified': {'read_only': True},
        }

    def validate_password(self, value):
        validate_password(value)
        return value
