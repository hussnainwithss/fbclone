from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from . import views
app_name = 'user_profile'
urlpatterns = [
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('', views.IndexView.as_view(), name='index'),
    path('update-profile-picture/', views.UpdateProfilePictureView.as_view(),
         name='update-profile-picture'),
    path('update-cover-picture/', views.UpdateCoverPictureView.as_view(),
         name='update-cover-picture'),
    path('update-profile/', views.UpdateProfileView.as_view(), name='update-profile'),
    path('user-feed/<int:user_id>', views.UserFeedView.as_view(), name='user-feed'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('create-post/', views.CreatePostView.as_view(), name='create-post')
]
