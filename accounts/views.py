from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages




# Create your views here.

class Login(View):

    def post(self,request,*args,**kwargs):
        
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
            messages.error(request,'Incorect Email/Password! Please try again!')
            return redirect("user_profile:index")
        return redirect("user_profile:dashboard")


class Logout(View):
    def post(self,request,*args,**kwargs):
        try:
            logout(request)
            messages.success(request,'Logout Successful!')
        except:
            messages.error(request,"Something went Wrong!")
        return redirect('user_profile:index')
