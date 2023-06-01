from django.urls import path

# from .views import (
# BrandOnlyView, InfluencerOnlyView,
# )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    UserCreateView,
    BrandOnlyView,
    InfluencerOnlyView,
    BrandProfileUpdateView,
    InfluencerProfileUpdateView,
    ProfilePictureView,
    ProfilePictureUpdateView,
    BrandProfileView,
    InfluencerProfileView,
    CampaignListCreateView,
    # CampaignRetrieveUpdateDestroyView,
    CampaignUpdateDestroyView,
    InfluencerPoolView,
    CreateInfluencerPool,
    JobListCreateView,
    JobRetrieveUpdateDestroyView,
    data_deletion_callback,
)

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path('brand/<str:username>/', BrandOnlyView.as_view(), name='brand'),
    # path('influencer/<str:username>/', InfluencerOnlyView.as_view(), name='influencer'),
    path("users/create/", UserCreateView.as_view(), name="user_create"),
    path("brand-only/", BrandOnlyView.as_view(), name="brand_only"),
    path("influencer-only/", InfluencerOnlyView.as_view(), name="influencer"),
    path("brand/", BrandProfileView.as_view(), name="brand"),
    path("influencer/", InfluencerProfileView.as_view(), name="influencer"),
    path(
        "brand-profile-update/",
        BrandProfileUpdateView.as_view(),
        name="brand_profile_update",
    ),
    path(
        "influencer-profile-update/",
        InfluencerProfileUpdateView.as_view(),
        name="influencer_profile_update",
    ),
    path("profile-picture-view/", ProfilePictureView.as_view(), name="view-profile"),
    path(
        "profile-picture/",
        ProfilePictureUpdateView.as_view(),
        name="profile_picture_update",
    ),
    # campaigns
    path("campaigns/", CampaignListCreateView.as_view(), name="campaigns_list_create"),
    path(
        "campaigns/<int:pk>/",
        CampaignUpdateDestroyView.as_view(),
        name="campaigns_retrieve_update_destroy",
    ),
    path("jobs/", JobListCreateView.as_view(), name="jobs_list_create"),
    path(
        "jobs/<int:pk>/",
        JobRetrieveUpdateDestroyView.as_view(),
        name="jobs_retrieve_update_destroy",
    ),
    path(
        "campaigns/<int:campaign_id>/influencer-pool/",
        InfluencerPoolView.as_view(),
        name="influencer_pool_list",
    ),
    path("influencerpool/", CreateInfluencerPool.as_view(), name="create-pool"),
    path(
        "data-deletion-callback/", data_deletion_callback, name="data_deletion_callback"
    ),
]
