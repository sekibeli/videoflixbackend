# from django.test import TestCase
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from .models import Video
# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token

# from django.contrib.auth import get_user_model
# User = get_user_model()


from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class TestAuthenticationRequired(APITestCase):
    def test_list_videos_requires_authentication(self):
        url = reverse('video-list')  # Ersetze 'video-list' durch den tatsächlichen Namen der URL in deinen urls.py, wenn er anders ist
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestVideoList(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('video-list')  # Ersetze 'video-list' entsprechend

    def test_retrieve_video_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        

class TestAddNewVideo(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='test134password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('video-list')  # Ersetze 'video-list' entsprechend

    def test_add_new_video_with_file(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        video_path = os.path.join(BASE_DIR, 'media/videos/160702_540p.mp4')
        video_data = SimpleUploadedFile(name='test_video.mp4', content=open(video_path, 'rb').read(), content_type='video/mp4')
        
        data = {
            'title': 'Test Video',
            'description': 'A test video description',
            'isVisible': True,
            'video_file': video_data,
            'category': 'allgemein'
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('video_file' in response.data)
        self.assertEqual(response.data['category'], 'allgemein')
        self.assertTrue(response.data['isVisible'])
