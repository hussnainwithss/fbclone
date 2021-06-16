from django.contrib import messages
from django.http import request
from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.views import View
from django.views.generic import TemplateView
from . import models
from . import forms

# Create your views here.


class IndexView(View):
    def get(self,request, *args, **kwargs):
        try:
            if request.user.is_authenticated and models.UserProfile.objects.get(user=request.user):
                return redirect('user_profile:dashboard')
        except models.UserProfile.DoesNotExist:
            return render(request,'pages/index.html')
        return render(request,'pages/index.html')    


class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'pages/profile.html'
    login_url = 'user_profile:index'
    
    
class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    login_url = 'user_profile:index'
    template_name = 'pages/update_profile.html'

    def post(self,request,*args,**kwargs):
        pass


class UpdateProfilePictureView(LoginRequiredMixin,View):
    login_url = 'user_profile:index'

    def post(self,request,*args,**kwargs):
        profile = request.user.profile
        form = forms.ProfilePictureForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile Picture Updated!')
        else:
            messages.error(request,"Something went wrong!")
        return redirect('user_profile:dashboard')


class UpdateCoverPictureView(LoginRequiredMixin,View):
    login_url = 'user_profile:index'

    def post(self,request,*args,**kwargs):
        profile = request.user.profile
        form = forms.CoverPictureForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,'Cover Picture Updated!')
        else:
            messages.error(request,"Something went wrong! ")
        return redirect('user_profile:dashboard')

class UpdateProfileView(LoginRequiredMixin,View):
    login_url = 'user_profile:index'

    def post(self,request,*args,**kwargs):
        profile = request.user.profile
        form = forms.ProfileUpdate(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            request.user.first_name = form.cleaned_data['first_name'] if form.cleaned_data['first_name'] != request.user.first_name else request.user.first_name
            request.user.last_name = form.cleaned_data['last_name'] if form.cleaned_data['last_name'] != request.user.last_name else request.user.last_name
            request.user.email = form.cleaned_data['email'] if form.cleaned_data['email'] != request.user.email else request.user.email
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request,'Profile Info Updated Successfully!')
        else:
            print(form.errors)
            messages.error(request,"Something went wrong! ")
        return redirect('user_profile:dashboard')

        

