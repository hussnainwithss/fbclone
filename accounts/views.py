from django.db.utils import IntegrityError
from user_profile.models import UserProfile,FeedTemplate,Feed
from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from . import managers,models


# Create your views here.

class Login(View):

    def post(self,request,*args,**kwargs):
        if 'email' in request.session:
            del request.session['email']
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,email=email,password=password) 
        if user is not None and user.is_active:
            login(request,user)
            if not request.POST.get('remember-me', None):
                request.session.set_expiry(0)
                request.session.modified = True
            messages.success(request,'Login Successful!')
        else:
            request.session['email'] = email
            messages.error(request,'Incorect Email/Password! Please try again!')
            return  redirect("user_profile:index")
        return redirect("user_profile:settings")


class Logout(View):
    def post(self,request,*args,**kwargs):
        try:
            logout(request)
            messages.success(request,'Logout Successful!')
        except:
            messages.error(request,"Something went Wrong!")
        return redirect('user_profile:index')


class Register(View):
    def post(self,request,*args,**kwargs):
        REGISTERED_FEED_CONTENT = '{full_name} has joined UBook'
        if 'email' in request.session:
            del request.session['email']
        
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        birthday = request.POST['birthday']
        gender=request.POST['gender']
        if password1 != password2:
            messages.warning(request,"Password and Confirm Password do not Match!")
            return redirect('user_profile:index')
        email = managers.CustomUserManager.normalize_email(email)
        user = None
        try:
            user = models.CustomUser.objects.create(email=email,first_name=first_name,last_name=last_name,is_active=True)
            user.set_password(password1)
            user_profile = UserProfile.objects.create(user=user,birthday=birthday,gender=gender)
            REGISTERED_FEED_CONTENT = REGISTERED_FEED_CONTENT.format(full_name=user.get_full_name())
            register_feed_template = FeedTemplate.objects.create(content=REGISTERED_FEED_CONTENT,feed_type='register')
            register_feed_object = Feed.objects.create(user=user,feed_template=register_feed_template)
            user.save()
            user_profile.save()
            register_feed_template.save()
            register_feed_object.save()
            user = authenticate(request,email=email,password=password1)
            if user is not None and user.is_active:
                login(request,user)
                request.session.set_expiry(0)
                request.session.modified = True
            messages.success(request,"Registration Successful! Welcome {}".format(user.get_full_name()))
            return redirect('user_profile:settings')
        except IntegrityError:
            messages.warning(request,"User Already Exists Try Logging in!")
            request.session['email'] = email

            return redirect('user_profile:index')
        except Exception as e:
            messages.warning(request,"Something Went Wrong! Please Try again!  {}".format(str(e)))
            return redirect('user_profile:index')
        

class ChangePasswordView(View):
    def post(self,request,*args,**kwargs):
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request, user)
            messages.success(request,'Password successfully updated!')
        else:
            messages.error(request, 'Please correct the errors below.')
            messages.error(request,form.errors.as_text())
        return redirect('user_profile:settings')
        