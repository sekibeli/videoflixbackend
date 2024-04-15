import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# Create your models here.
class CustomUser(AbstractUser):
    is_verified = models.BooleanField(default=False)
    adress = models.CharField(max_length=150, default='')
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    liked_videos = models.ManyToManyField('videoflixbackend.Video', related_name='liked_videos', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    is_guest = models.BooleanField(default=False)