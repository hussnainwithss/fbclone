from django import contrib
from django.contrib import messages
from django.http import request
from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.views import View
from django.views.generic import TemplateView,ListView
from django.db.models import Q
from accounts.models import CustomUser
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


class SettingsView(LoginRequiredMixin,TemplateView):
    template_name = 'pages/profile.html'
    login_url = 'user_profile:index'
    
    
class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'pages/dashboard.html'
    login_url = 'user_profile:index'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feed_objects'] = models.Feed.objects.filter(user_id=self.request.user.id)
        return context

   
class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    login_url = 'user_profile:index'
    template_name = 'pages/update_profile.html'

    

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
        return redirect('user_profile:settings')


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
        return redirect('user_profile:settings')

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
        return redirect('user_profile:settings')

        

class UserFeedView(TemplateView,LoginRequiredMixin):
    login_url = 'user_profile:index'
    template_name = 'pages/user_feed.html'

    def get(self,request,user_id,*args,**kwargs):
        if user_id == request.user.id:
                return redirect('user_profile:settings')
        context = super(UserFeedView,self).get_context_data(*args,**kwargs)
        try: 
            context['feed_user'] = CustomUser.objects.get(id=user_id)
            if context['feed_user'].is_staff or context['feed_user'].is_superuser:
                raise CustomUser.DoesNotExist
        except CustomUser.DoesNotExist:
            messages.error(request,"User with user_id={} doesnt Exist!".format(user_id))
            return redirect('user_profile:settings')
        try:
            context['feed_objects'] = models.Feed.objects.filter(user_id=user_id)
            print(context['feed_objects'])
        except:
            messages.error(request,"Error Loading Feed for this user")
        return render(request,template_name=self.template_name,context=context)
    

class SearchView(ListView, LoginRequiredMixin):
    login_url = 'user_profile:index'
    template_name = 'pages/search.html'
    model = CustomUser
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(~Q(is_staff = True) and ~Q(is_superuser = True), ~Q(id=self.request.user.id))
        return qs.filter(Q(first_name__icontains=self.request.GET['search_query']) | Q(last_name__icontains=self.request.GET['search_query']))
        

class CreatePostView(LoginRequiredMixin,View):
    login_url = 'user_profile:index'
    ADD_NEW_PHOTO = 'add_new_photo'
    ADD_NEW_TEXT = 'add_new_text'

    def post(self,request,*args,**kwargs):
        form = forms.CreatePostForm(request.POST,request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            print(form.cleaned_data['image'] != None)
            form.cleaned_data['feed_type'] = self.ADD_NEW_PHOTO if form.cleaned_data['image'] != None else self.ADD_NEW_TEXT
            print(form.cleaned_data['feed_type'])
            print(form.cleaned_data)
            feed_template = form.save()
            print(feed_template)
            feed_obj = models.Feed.objects.create(feed_template=feed_template,user=request.user)
            feed_obj.save()
            messages.success(request,"Update Successfully Posted")
        else:
            messages.warning(request,'something went wrong try again')
        return redirect('user_profile:dashboard')
        