from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages




# Create your views here.

class Login(View):

    def post(self,request,*args,**kwargs):
        username = request.POST['username']
        password = request.POST['password']
        remember_me = True if 'remember' in request.POST else False

        user = authenticate(request,username=username,password=password) 
        if user is not None and user.is_active:
            login(request,user)
            if not remember_me:
                request.session.set_expiry(0)
                request.session.modified = True
            messages.success(request,'Login Successful!')
        else:
            messages.error(request,'Incorect Username/Password! Please try again!')
            
        return redirect("index")