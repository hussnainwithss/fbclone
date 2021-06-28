from django.urls import path
from rest_framework.authtoken import views
from apis.views import (UserRegistrationView, UserPasswordChangeView,
                        UserProfileUpdateView, UserProfilePicturesUpdateView, UserPostCreateView, UserSearchView)
app_name = 'api'

urlpatterns = [
    path('login/', views.obtain_auth_token),
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('change-password/', UserPasswordChangeView.as_view(),
         name='change_password'),
    path('update-profile/', UserProfileUpdateView.as_view(), name='update_profile'),
    path('update-profile-pictures/', UserProfilePicturesUpdateView.as_view(),
         name='update_profile_pictures'),
    path('create-post/', UserPostCreateView.as_view(), name='create_post'),
    path('search/', UserSearchView.as_view(), name='search')
]
