from django.db.utils import IntegrityError
from django.dispatch import Signal
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from user_profile.models import UserProfile, FeedTemplate, Post
from accounts import managers, models


user_profile_create_signal = Signal(
    providing_args=['user', 'birthday', 'gender'])

# Create your views here.


class Login(View):
    """ VIew for Handling Login
    Only supports Post requests on authentication
    the session is logged and the user is redirected to dashboard
    else user is redirected to loginpage with error
    """

    def post(self, request, *args, **kwargs):
        if 'email' in request.session:
            del request.session['email']
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if not request.POST.get('remember-me', None):
                # logic for making the user logout as soon as browser is closed
                # if remember me is not checked on login
                request.session.set_expiry(0)
                request.session.modified = True
            messages.success(request, 'Login Successful!')
        else:
            request.session['email'] = email
            messages.error(
                request, 'Incorect Email/Password! Please try again!')
            return redirect("user_profile:index")
        return redirect("user_profile:dashboard")


class Logout(View, LoginRequiredMixin):
    """ VIew for Handling logout
    Only supports Post requests
    logouts the user when endpoint is accessed else
    throws error. User must be logged in to logout
    """
    login_url = 'user_profile:index'

    def post(self, request, *args, **kwargs):
        try:
            logout(request)
            messages.success(request, 'Logout Successful!')
        except Exception as e:
            messages.error(request, "Something went Wrong! {}".format(e))
        return redirect('user_profile:index')


class Register(View):
    """View for User registration
    only supports POST Method
    creates the necessary db objects
    logs the user in and redirect the user
    to the dashboard else redirects back to
    signup page
    """

    def post(self, request, *args, **kwargs):
        if 'email' in request.session:
            del request.session['email']

        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        birthday = request.POST['birthday']
        gender = request.POST['gender']
        if password1 != password2:
            messages.warning(
                request, "Password and Confirm Password do not Match!")
            return redirect('user_profile:index')
        email = managers.CustomUserManager.normalize_email(email)
        user = None
        try:
            user = models.CustomUser.objects.create_user(
                email=email, first_name=first_name, last_name=last_name, password=password1, is_active=True)
            user_profile_create_signal.send(
                sender=self.__class__, user=user, birthday=birthday, gender=gender)
            user = authenticate(request, email=email, password=password1)
            if user is not None and user.is_active:
                login(request, user)
                request.session.set_expiry(0)
                request.session.modified = True
            messages.success(
                request, "Registration Successful! Welcome {}".format(user.get_full_name()))
            return redirect('user_profile:dashboard')
        except IntegrityError:
            messages.warning(request, "User Already Exists Try Logging in!")
            request.session['email'] = email

            return redirect('user_profile:index')
        except Exception as exeception:
            messages.warning(
                request, "Something Went Wrong! Please Try again!  {}".format(str(exeception)))
            return redirect('user_profile:index')


class ChangePasswordView(View):
    """
    Password change view
    Only accepts POST requests
    Uses django's default password change form
    once verfies form data changes password and
    recommutes and updates session hash so that user
    isnt logged out
    """

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password successfully updated!')
        else:
            messages.error(request, 'Please correct the errors below.')
            messages.error(request, form.errors.as_text())
        return redirect('user_profile:dashboard')
