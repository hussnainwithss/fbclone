from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, serializers
from rest_framework import status
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from apis.serializers import (UserRegistrationSerializer, UserPasswordChangeSerializer,
                              UserProfileUpdateSerializer, UserProfilePicturesUpdateSerializer, FeedTemplateSerializer, UserSerializer)
from apis.permissions import IsProfileOwnerOrReadOnly
from user_profile.models import FeedTemplate, UserProfile
from apis.filters import UserFilterSet
User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    class Meta:
        model = User


class UserPasswordChangeView(generics.UpdateAPIView):
    serializer_class = UserPasswordChangeSerializer

    class Meta:
        model = User

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UserProfileUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsProfileOwnerOrReadOnly)
    serializer_class = UserProfileUpdateSerializer

    class Meta:
        model = User

    def get_object(self):
        return self.request.user


class UserProfilePicturesUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsProfileOwnerOrReadOnly)
    serializer_class = UserProfilePicturesUpdateSerializer

    class Meta:
        model = UserProfile

    def get_object(self):
        return self.request.user.profile


class UserPostListCreateView(generics.ListCreateAPIView):
    serializer_class = FeedTemplateSerializer

    class Meta:
        model = FeedTemplate

    def get_queryset(self):
        user_id = self.request.query_params.get('id', self.request.user.id)
        return FeedTemplate.objects.filter(feed_template__user_id=user_id).order_by('-created_at')


class UserSearchView(generics.ListAPIView):
    def get_queryset(self):
        return User.objects.filter(~Q(id=self.request.user.id), is_staff=False, is_superuser=False)
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['first_name', 'last_name']
    filterset_class = UserFilterSet

    class Meta:
        model = User


class UserRetrieveView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    class Meta:
        model = User

    def get_object(self):
        if self.request.query_params.get('id', None):
            return User.objects.get(id=self.request.query_params.get('id'))
        return self.request.user
