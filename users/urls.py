from django.urls import re_path
from .views import ( InfluencerSignupView, DemoSignupView,
 BrandSignupView, EmployeeSignupView,
 CustomAuthToken, 
 LogoutView, BrandOnlyView, InfluencerOnlyView, DeleteAccountView,
 GetUserProfileView, VerifyEmail, #UpdateUserProfileView, #UpdateProfilePicView, 
 #LoginView
 )

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

# have to comment out the Url path for the code to debug

    #re_path(r'update', UpdateUserProfileView.as_view(), name='update'),
    #re_path(r'profile_pic', UpdateProfilePicView.as_view(), name='profile_pic'),

    re_path(r'influencer/dashboard', InfluencerOnlyView.as_view(), name='influencer-dashboard'),
    re_path(r'brand/dashboard', BrandOnlyView.as_view(), name='brand-dashboard'),
    re_path(r'employee/dashboard', EmployeeSignupView.as_view(), name='employee-dashboard'),
]