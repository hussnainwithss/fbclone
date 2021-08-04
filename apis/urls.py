from django.urls import path
from rest_framework.authtoken import views
from apis.views import (UserRegistrationView, UserPasswordChangeView,
                        UserProfileUpdateView, UserProfilePicturesUpdateView, UserPostListCreateView, UserSearchView, UserRetrieveView)
app_name = 'api'

urlpatterns = [
    path('login/', views.obtain_auth_token, name='user_login'),
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('change-password/', UserPasswordChangeView.as_view(),
         name='change_password'),
    path('update-profile/', UserProfileUpdateView.as_view(), name='update_profile'),
    path('update-profile-pictures/', UserProfilePicturesUpdateView.as_view(),
         name='update_profile_pictures'),
    path('post/', UserPostListCreateView.as_view(), name='post'),
    path('search/', UserSearchView.as_view(), name='search'),
    path('user/', UserRetrieveView.as_view(), name='user')
]
