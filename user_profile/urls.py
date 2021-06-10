from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from . import views
app_name = 'user_profile'
urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(template_name = 'pages/dashboard.html'), name='dashboard'),
    path('',views.IndexView.as_view(),name='index')
]
