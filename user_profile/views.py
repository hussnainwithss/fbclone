from accounts.views import Login
from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView

# Create your views here.


class IndexView(View):
    def get(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user_profile:dashboard')
        return render(request,'pages/index.html')


class DashboardView(LoginRequiredMixin,TemplateView):
    login_url = 'user_profile:index'
    

