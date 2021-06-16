from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from . import views
app_name = 'user_profile'
urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('',views.IndexView.as_view(),name='index'),
    path('update-profile-picture/',views.UpdateProfilePictureView.as_view(),name='update-profile-picture'),
    path('update-cover-picture/',views.UpdateCoverPictureView.as_view(),name='update-cover-picture'),
    path('update-profile/',views.UpdateProfileView.as_view(),name='update-profile'),
    

]
