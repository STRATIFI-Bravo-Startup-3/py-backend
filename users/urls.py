from django.urls import re_path, path
from .views import (InfluencerSignupView,
BrandSignupView,EmployeeSignupView,BrandListCreateView,
BrandDetailView,CustomAuthToken, EmployeeListCreateView,
EmployeeDetailView, InfluencerListCreateView,InfluencerDetailView,
LogoutView, BrandOnlyView, InfluencerOnlyView, DeleteAccountView,
#GetUserProfileView, 
VerifyEmail, UpdateProfilePicView,
UpdateProfilePicViewDetailView,#UpdateUserProfileView,
BrandSignupView, EmployeeSignupView,
CustomAuthToken,LogoutView, BrandOnlyView, 
InfluencerOnlyView, DeleteAccountView,
#GetUserProfileView, 
VerifyEmail, ChangePasswordView,
user_detail_view, 
#user_redirect_view, 
user_update_view,
#custom_token_auth,
) #(UpdateUserProfileView, #UpdateProfilePicView,
 #LoginView

app_name = "users"

urlpatterns=[
    re_path(r'signup/influencer', InfluencerSignupView.as_view()),
    re_path(r'signup/brand', BrandSignupView.as_view()),
    re_path(r'employee/signup', EmployeeSignupView.as_view()),

    re_path(r'signup/verify-email', VerifyEmail.as_view(),name='verify-email'),
    
 #   re_path(r'signin', view=custom_token_auth, name='signin'),
    re_path(r'login',CustomAuthToken.as_view()),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    #re_path(r'login', LoginView.as_view()),

    #re_path(r'wherenext/$', wherenext, name='wherenext'),
    re_path(r'logout', LogoutView.as_view(), name='logout-view'),

    re_path(r'delete', DeleteAccountView.as_view(), name='delete-account'),

    #re_path(r'user', GetUserProfileView.as_view()),
    
    #re_path(r'update', UpdateUserProfileView.as_view(), name='update'),
    
    re_path(r'profile_pic', UpdateProfilePicView.as_view(), name='profile_pic'),
    path('profile/<int:pk>/', UpdateProfilePicViewDetailView.as_view(), name='profile_pic'),

    re_path(r'all-brand/', BrandListCreateView.as_view(), name='brand-list'),
    path('brand/<int:pk>/', BrandDetailView.as_view(), name='brand'),
    
    re_path(r'all-employee/', EmployeeListCreateView.as_view(), name='employee-list'),
    path('employee/<int:pk>/', EmployeeDetailView.as_view(), name='employee'),

    re_path(r'all-influencer/', InfluencerListCreateView.as_view(), name='influencer-list'),
    path('influencer/<int:pk>/', InfluencerDetailView.as_view(), name='influencer'),

# have to comment out the Url path for the code to debug

    #re_path(r'update', UpdateUserProfileView.as_view(), name='update'),
    #re_path(r'profile_pic', UpdateProfilePicView.as_view(), name='profile_pic'),
    re_path(r'influencer/dashboard', InfluencerOnlyView.as_view(), name='influencer-dashboard'),
    re_path(r'brand/dashboard', BrandOnlyView.as_view(), name='brand-dashboard'),
    re_path(r'employee/dashboard', EmployeeSignupView.as_view(), name='employee-dashboard'),
 

    #check this out
    #re_path(r"~redirect/", view=user_redirect_view, name="redirect"),
    re_path(r"~update/", view=user_update_view, name="update"),
    re_path(r"<str:username>/", view=user_detail_view, name="detail"),

]

'''
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views as auth_views
from .views import (
    BrandListCreateView, 
    BrandDetailView, 
    EmployeeListCreateView, 
    EmployeeDetailView,
    InfluencerListCreateView,
    InfluencerDetailView,
    UpdateProfilePicView,
    UpdateProfilePicViewDetailView,
    UserViewSet,
    DashboardView,
    PasswordResetView,
    PasswordResetConfirmView
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', auth_views.obtain_auth_token),
    path('brands/', BrandListCreateView.as_view(), name='brand_list_create'),
    path('brands/<int:pk>/', BrandDetailView.as_view(), name='brand_detail'),
    path('employees/', EmployeeListCreateView.as_view(), name='employee_list_create'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('influencers/', InfluencerListCreateView.as_view(), name='influencer_list_create'),
    path('influencers/<int:pk>/', InfluencerDetailView.as_view(), name='influencer_detail'),
    path('update-profile-pic/', UpdateProfilePicView.as_view(), name='update_profile_pic'),
    path('update-profile-pic/<int:pk>/', UpdateProfilePicViewDetailView.as_view(), name='update_profile_pic_detail'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm')
]

'''
