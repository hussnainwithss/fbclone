from django.urls import path,reverse_lazy
from django.contrib.auth import views as auth_views

from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/',views.Logout.as_view(),name='logout'),
    path('register',views.Register.as_view(),name='register'),
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('accounts:password_reset_done'),template_name='registration/password_reset_form.html'), name ='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('accounts:password_reset_complete')), name ='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name ='password_reset_complete'),
    path('password_change/',auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('accounts:password_change_done')),name='password_change'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('change_password/',views.ChangePasswordView.as_view(),name='change_password')


]
