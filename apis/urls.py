from django.urls import path
from rest_framework.authtoken import views
app_name = 'api'

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token)
]
