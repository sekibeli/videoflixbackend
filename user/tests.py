from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.core import mail
from django.contrib.auth.tokens import default_token_generator

from videoflixbackend.models import Video
from user.models import CustomUser

from django.core.files.base import ContentFile


class LoginTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.user.is_verified = True
        self.user.save()

    def test_successful_login(self):
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
    
    def test_login_wrong_password(self):
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue('error' in response.data)

    def test_login_wrong_username(self):
        url = reverse('login')
        data = {'username': 'wrongusername', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue('error' in response.data)
        
        
class SignupTests(APITestCase):
    def setUp(self):
        self.signup_url = reverse('signup')  

    def test_successful_signup(self):
        data = {
            'username': 'neuerbenutzer',
            'email': 'neu@example.com',
            'password': 'ksfsduf1531--.,'
        }
        response = self.client.post(self.signup_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email='neu@example.com').exists())
        self.assertEqual(len(mail.outbox), 1) 
        self.assertIn('Please confirm your email', mail.outbox[0].subject)

    def test_signup_existing_email(self):
        CustomUser.objects.create_user(username='existinguser', email='existing@example.com', password='testpassword123')

        data = {
        'username': 'newuser',
        'email': 'existing@example.com',  # Gleiche E-Mail wie oben
        'password': 'ksfsduf1531--.,'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, "An error occured", status_code=status.HTTP_400_BAD_REQUEST)


    def test_signup_short_password(self):
        data = {
            'username': 'userwithshortpass',
            'email': 'shortpass@example.com',
            'password': 'short'  # Passwort ist zu kurz
        }
        response = self.client.post(self.signup_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, "This password is too short", status_code=status.HTTP_400_BAD_REQUEST)
