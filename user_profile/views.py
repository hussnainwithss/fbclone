import json
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.views import View
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from accounts.models import CustomUser
from user_profile import models, forms


# Create your views here.


class IndexView(View):
    """Main Index View that renders the
    index page. if user is already logged in
    they are redirected to dashboard else to
    main index page with signin and signup options
    """

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            return redirect('user_profile:dashboard')
        return render(request, 'pages/index.html')


class SettingsView(LoginRequiredMixin, TemplateView):
    """
    Settings Views Extends the Template view
    and renders the user settings update page
    Login is required to change user settings hence
    LoginRequiredMixin
    """
    template_name = 'pages/profile.html'
    login_url = 'user_profile:index'


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Dashboard Views Extends the Template view
    and renders the main dashboard for logged in user
    with user's feed and basic info
    Login is required henceLoginRequiredMixin
    """
    template_name = 'pages/dashboard.html'
    login_url = 'user_profile:index'

    def get_context_data(self, **kwargs):
        """
        Overridden get_context_data method
        to include the original context data
        as well as the user feed objects
        which will be displayed
        P.S. Can be better implemented using a ListView
        rather than a templateView
        """
        context = super().get_context_data(**kwargs)
        context['feed_objects'] = models.Post.objects.filter(
            user_id=self.request.user.id)
        return context


class UpdateProfilePictureView(LoginRequiredMixin, View):
    """
    Update ProfilePicture View
    for updating user profile picture
    accepts only POST requests
    uses ProfilePictureForm that handles the update
    """
    login_url = 'user_profile:index'

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        form = forms.ProfilePictureForm(
            request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Picture Updated!')
        else:
            messages.error(request, "Something went wrong!")
        return redirect('user_profile:settings')


class UpdateCoverPictureView(LoginRequiredMixin, View):
    """
    Update CoverPicture View
    for updating user Cover picture
    accepts only POST requests
    uses ProfileCoverForm that handles the update
    """
    login_url = 'user_profile:index'

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        form = forms.CoverPictureForm(
            request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cover Picture Updated!')
        else:
            messages.error(request, "Something went wrong! ")
        return redirect('user_profile:settings')


class UpdateProfileView(LoginRequiredMixin, View):
    """
    Update user Profile View
    for updating user profile
    (proerties such as bio, education etc)
    accepts only POST requests
    uses ProfileUpdateform that handles the update
    """
    login_url = 'user_profile:index'

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        form = forms.ProfileUpdate(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Profile Info Updated Successfully!')
        else:
            messages.error(request, "Something went wrong! ")
        return redirect('user_profile:settings')


class UserFeedView(TemplateView, LoginRequiredMixin):
    """
    User Feed View that renders the user feed
    Only supports get request
    takes the user id as argument and return and renders
    feed objects for that user
    ]
    """
    login_url = 'user_profile:index'
    template_name = 'pages/user_feed.html'

    def get(self, request, user_id, *args, **kwargs):
        if user_id == request.user.id:
            return redirect('user_profile:settings')
        context = super(UserFeedView, self).get_context_data(*args, **kwargs)
        try:
            context['feed_user'] = CustomUser.objects.get(id=user_id)
            if context['feed_user'].is_staff or context['feed_user'].is_superuser:
                raise CustomUser.DoesNotExist
        except CustomUser.DoesNotExist:
            messages.error(
                request, "User with user_id={} doesnt Exist!".format(user_id))
            return redirect('user_profile:settings')
        try:
            context['feed_objects'] = models.Post.objects.filter(
                user_id=user_id)
        except Exception:
            messages.error(request, "Error Loading Feed for this user")
        return render(request, template_name=self.template_name, context=context)


class SearchView(ListView, LoginRequiredMixin):
    """
    User Search View
    Inherits from ListView and LoginRequiredMixin
    supports both get and post request
    the post request is an ajax call
    """
    login_url = 'user_profile:index'
    template_name = 'pages/search.html'
    model = models.UserProfile

    def get_queryset(self):
        """
        Functions filters the search objects
        only shows users that match the search critera
        either first name or last name should contain the search keyword
        query is further filtered for users that are not staff or admin
        also the current user is filtered out of the results
        """
        qs = super().get_queryset()
        # filter to get users that match our criteria
        query = self.request.GET['search_query'] if self.request.GET.get(
            'search_query', None) else self.request.POST['search_query']  # in case of ajax request post contains query else get contains
        qs = qs.filter(Q(user__first_name__icontains=query)
                       | Q(user__last_name__icontains=query))
        qs = qs.filter(~Q(user__is_staff=True) and ~Q(
            user__is_superuser=True), ~Q(user__id=self.request.user.id))  # filter non admin users out and remove current logged in user
        return qs

    def get_context_data(self, **kwargs):
        """
        Method to add additional context data 
        for the side filters
        we only wanna include values that are present in the search results
        to be present in the filters hence these filtering
        """
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET['search_query']
        context['hometowns'] = self.get_queryset().filter(
            ~Q(hometown='')).values_list('hometown', flat=True).distinct()
        context['works'] = self.get_queryset().filter(
            ~Q(work='')).values_list('work', flat=True).distinct()
        context['educations'] = self.get_queryset().filter(
            ~Q(education='')).values_list('education', flat=True).distinct()
        return context

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax:
            search_filters = {}
            search_filters['education'] = self.request.POST.get(
                'education', None)
            search_filters['work'] = self.request.POST.get('work', None)
            search_filters['hometown'] = self.request.POST.get(
                'hometown', None)
            search_filters['gender'] = self.request.POST.get('gender', None)
            search_filters['relationship_status'] = self.request.POST.get(
                'relationship_status', None)
            try:
                search_filters = {k: v for k,
                                  v in search_filters.items() if v is not None}  # only keep keys that have not None values
                qs = self.get_queryset().filter(**search_filters)
                response = serializers.serialize(
                    'json', qs)  # serialize values
                # convert into dict to add more values
                response = json.loads(response)
                for obj in response:
                    obj['fields']['user'] = {
                        'id': obj['fields']['user'],
                        'name': CustomUser.objects.get(id=obj['fields']['user']).get_full_name()
                    }
                    # add user name and age fields
                    obj['fields']['age'] = qs.get(id=obj['pk']).get_age()
                return JsonResponse({"response": response}, status=200)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        return JsonResponse({"error": "Invalid request"}, status=400)


class CreatePostView(LoginRequiredMixin, View):
    """
    CreatePostView Handles post creation by user
    Login is required
    currently two types of posts are supported
    only supports post method
    """
    login_url = 'user_profile:index'
    ADD_NEW_PHOTO = 'add_new_photo'
    ADD_NEW_TEXT = 'add_new_text'

    def post(self, request, *args, **kwargs):
        form = forms.CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            feed_template = form.save()
            feed_obj = models.Post.objects.create(
                feed_template=feed_template, user=request.user)
            feed_obj.save()
            messages.success(request, "Update Successfully Posted")
        else:
            messages.warning(request, 'something went wrong try again')
        return redirect('user_profile:dashboard')
