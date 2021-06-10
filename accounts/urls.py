from django.urls import path
import django.contrib.auth.views as auth_views
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    
]
