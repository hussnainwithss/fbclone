from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views.decorators.csrf import requires_csrf_token
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
User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    class Meta:
        model = User

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_gender = serializer.validated_data.get('gender')
            user_birthday = serializer.validated_data.get('birthday')
            user = User.objects.create_user(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            user.first_name = serializer.validated_data['first_name']
            user.last_name = serializer.validated_data['last_name']
            user.save()
            user_profile = UserProfile.objects.create(
                user=user, gender=user_gender, birthday=user_birthday)
            user_profile.save()
            response = serializer.validated_data
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordChangeView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPasswordChangeSerializer

    class Meta:
        model = User

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            if hasattr(user, 'auth_token'):
                user.auth_token.delete()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserProfileUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsProfileOwnerOrReadOnly)
    serializer_class = UserProfileUpdateSerializer

    class Meta:
        model = User

    def get_object(self):
        return self.request.user

    def patch(self, request,  *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfilePicturesUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsProfileOwnerOrReadOnly)
    serializer_class = UserProfilePicturesUpdateSerializer

    class Meta:
        model = UserProfile

    def get_object(self):
        return self.request.user.profile


class UserPostCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FeedTemplateSerializer

    class Meta:
        model = FeedTemplate

    def list(self,   *args, **kwargs):
        user_id = self.request.query_params.get('id', self.request.user.id)
        serializer = self.get_serializer(
            FeedTemplate.objects.filter(feed_template__user__id=user_id), many=True)
        return Response(serializer.data)


class UserSearchView(generics.ListAPIView):
    def get_queryset(self):
        return CustomUser.objects.filter(~Q(id=self.request.user.id), is_staff=False, is_superuser=False)
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['first_name', 'last_name']
    filterset_fields = ['profile__education',
                        'profile__gender', 'profile__work', 'profile__relationship_status', 'profile__hometown']

    class Meta:
        model = CustomUser
