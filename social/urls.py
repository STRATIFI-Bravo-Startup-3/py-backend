from django.urls import path

from .views import (SocialMediaHandleList, SocialMediaHandleDetail, SocialMediaPlatformList, twitter_profile,
                    instagram_profile, facebook_profile, tiktok_profile, youtube_profile)

urlpatterns = [
    path('platforms/', SocialMediaPlatformList.as_view(), name='socialmedia-platform-list'),
    path('handles/', SocialMediaHandleList.as_view(), name='socialmedia-handle-list'),
    path('handles/<int:pk>/', SocialMediaHandleDetail.as_view(), name='socialmedia-handle-detail'),
    path('handles/<int:handle_id>/twitter-profile/', twitter_profile, name='socialmedia-twitter-profile'),
    path('handles/<int:handle_id>/instagram-profile/', instagram_profile, name='socialmedia-instagram-profile'),
    path('handles/<int:handle_id>/facebook-profile/', facebook_profile, name='socialmedia-facebook-profile'),
    path('handles/<int:handle_id>/tiktok-profile/', tiktok_profile, name='socialmedia-tiktok-profile'),
    path('handles/<int:handle_id>/youtube-profile/', youtube_profile, name='socialmedia-youtube-profile'),
]
