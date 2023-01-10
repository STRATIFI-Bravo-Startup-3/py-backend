from django.urls import re_path, path
from .views import (InfluencerSignupView, DemoSignupView,
 BrandSignupView, EmployeeSignupView, BrandListCreateView, BrandDetailView,
 CustomAuthToken, EmployeeListCreateView, EmployeeDetailView, InfluencerListCreateView,
 InfluencerDetailView,LogoutView, BrandOnlyView, InfluencerOnlyView, DeleteAccountView,
 GetUserProfileView, VerifyEmail, UpdateProfilePicView, UpdateProfilePicViewDetailView,) #UpdateUserProfileView,
 #LoginView

urlpatterns=[
    re_path(r'signup/influencer', InfluencerSignupView.as_view()),
    re_path(r'signup/brand', BrandSignupView.as_view()),
    re_path(r'employee/signup', EmployeeSignupView.as_view()),
    re_path(r'signup/demo', DemoSignupView.as_view()),

    re_path(r'signup/verify-email', VerifyEmail.as_view(),name='verify-email'),
    
    re_path(r'login',CustomAuthToken.as_view()),

    #re_path(r'login', LoginView.as_view()),

    #re_path(r'wherenext/$', wherenext, name='wherenext'),
    re_path(r'logout', LogoutView.as_view(), name='logout-view'),

    re_path(r'delete', DeleteAccountView.as_view(), name='delete-account'),

    re_path(r'user', GetUserProfileView.as_view()),

    #re_path(r'update', UpdateUserProfileView.as_view(), name='update'),
    
    re_path(r'profile_pic', UpdateProfilePicView.as_view(), name='profile_pic'),
    path('profile/<int:pk>/', UpdateProfilePicViewDetailView.as_view(), name='profile_pic'),

    re_path(r'all-brand/', BrandListCreateView.as_view(), name='brand-list'),
    path('brand/<int:pk>/', BrandDetailView.as_view(), name='brand'),
    
    re_path(r'all-employee/', EmployeeListCreateView.as_view(), name='employee-list'),
    path('employee/<int:pk>/', EmployeeDetailView.as_view(), name='employee'),

    re_path(r'all-influencer/', InfluencerListCreateView.as_view(), name='influencer-list'),
    path('influencer/<int:pk>/', InfluencerDetailView.as_view(), name='influencer'),

    re_path(r'influencer/dashboard', InfluencerOnlyView.as_view(), name='influencer-dashboard'),
    re_path(r'brand/dashboard', BrandOnlyView.as_view(), name='brand-dashboard'),
    re_path(r'employee/dashboard', EmployeeSignupView.as_view(), name='employee-dashboard'),
]


