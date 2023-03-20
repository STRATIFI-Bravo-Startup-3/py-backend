from django.urls import path
from .views import SocialHandlesListCreateView, SocialHandlesDetailView

urlpatterns = [
    path('social-handles/', SocialHandlesListCreateView.as_view(), name='social_handles_list_create'),
    path('social-handles/<int:pk>/', SocialHandlesDetailView.as_view(), name='social_handles_detail'),
]
