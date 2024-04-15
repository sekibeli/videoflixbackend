"""
URL configuration for videoflix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


from rest_framework import routers

from user.views import (
    SignupView, 
    VerifyEmailView,
    LoginView,
    LogoutView,
    LoggeduserView,
    DeleteUserView,
    ToggleLike,
    GuestLoginView
)

from videoflixbackend.views import VideoViewSet, VideoSearchView


# router = routers.DefaultRouter()
# router.register(r'user', UserViewSet, basename='user')

router = routers.DefaultRouter()

router.register(r'videos', VideoViewSet, basename='video')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('videoflixbackend.urls')),
    path('api/password_reset/', include('django_rest_passwordreset.urls')),
    path('videos-search/', VideoSearchView.as_view(), name='videos-search'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('guest-login/', GuestLoginView.as_view(), name='guest-login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('edit-user/', LoggeduserView.as_view(), name='edit-user'),
    path('delete-user/', DeleteUserView.as_view(), name='delete-user'),
    path('toggle_like/<int:videoId>', ToggleLike.as_view(), name='toggle-like'),
    path('popular-videos/', VideoViewSet.as_view({'get': 'popular_videos'}), name='popular_videos'),
    path('mostSeen-videos/', VideoViewSet.as_view({'get': 'mostSeen_videos'}), name='mostSeen_videos'),
    path('recentVideos/', VideoViewSet.as_view({'get': 'recentVideos'}), name='recentVideos'),
    path('videos/<int:pk>/increment-view-count/', VideoViewSet.as_view({'post': 'increment_view_count'}), name='increment_view_count'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('django_rq/', include('django_rq.urls')),  
]  + static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
