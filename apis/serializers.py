from rest_framework.exceptions import ValidationError
from accounts.models import CustomUser
from datetime import date
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from user_profile.models import UserProfile, Post, FeedTemplate

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Others', 'Others')
    ]
    gender = serializers.ChoiceField(
        choices=GENDER_CHOICES, required=True)
    birthday = serializers.DateField(required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',
                  'password', 'confirm_password', 'gender', 'birthday']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'validators': [validate_password]
            },
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        if attrs['birthday'] > date.today():
            raise serializers.ValidationError(
                {"birthday": "Date of Birth cannot be greater than current date"}
            )
        return attrs

    def create(self, validated_data):
        p_ = validated_data.pop('confirm_password')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        _ = UserProfile.objects.create(
            user=user, gender=validated_data['gender'], birthday=validated_data['birthday'])
        return validated_data


class UserPasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_new_password = serializers.CharField(
        write_only=True, required=True)

    class Meta:
        model = User
        fields = ['current_password', 'new_password', 'confirm_new_password']

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                'Your old password was entered incorrectly. Please enter it again.'
            )
        return value

    def validate_confirm_new_password(self, value):
        if self.initial_data['new_password'] != value:
            raise serializers.ValidationError(
                "New Password and comfirm new password fields don't match."
            )
        return value

    def validate_new_password(self, value):
        validate_password(value)
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['bio', 'hometown', 'education', 'work',
                  'gender', 'birthday', 'relationship_status', 'profile_picture', 'cover_picture']
        extra_kwargs = {
            'gender': {
                'required': False
            },
            'birthday': {
                'required': False
            },
            'relationship_status': {
                'required': False
            },
            'profile_picture': {
                'read_only': True
            },
            'cover_picture': {
                'read_only': True
            }

        }
        model = UserProfile

    def validate_birthday(self, value):
        if value > date.today():
            raise serializers.ValidationError(
                {"birthday": "Date of Birth cannot be greater than current date"}
            )
        return value


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(partial=True, required=False)

    class Meta:
        fields = ['first_name', 'last_name', 'email', 'profile']
        extra_kwargs = {
            'first_name': {
                'required': False
            },
            'last_name': {
                'required': False
            },
            'email': {
                'required': False,
            },
            'profile': {
                'required': False
            }}
        model = User

    def update(self, instance, validated_data):
        if 'profile' in validated_data:
            profile_serializer = self.fields['profile']
            profile_instance = instance.profile
            profile_data = validated_data.pop('profile')

            profile_serializer.update(profile_instance, profile_data)
        return super(UserProfileUpdateSerializer, self).update(instance, validated_data)


class UserProfilePicturesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_picture']


class FeedTemplateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = FeedTemplate
        fields = ['user', 'content', 'image', 'feed_type']
        extra_kwargs = {
            'feed_type': {
                'read_only': True
            },
        }

    def validate(self, attrs):
        if not attrs.get('content', None) and not attrs.get('image', None):
            raise ValidationError({
                'message': 'Either add content or image!'})
        return attrs

    def create(self, validated_data):
        FEED_TYPE_DICT = {
            'add_new_photo': 'add_new_photo',
            'add_new_text': 'add_new_text',

        }
        feed_template_dict = {}
        if validated_data.get('content', None):
            feed_template_dict = {
                'content': validated_data['content']
            }
        if validated_data.get('image', None):
            feed_template_dict['image'] = validated_data['image']
            feed_template_dict['feed_type'] = FEED_TYPE_DICT['add_new_photo']
        else:
            feed_template_dict['feed_type'] = FEED_TYPE_DICT['add_new_text']
        feed_template = FeedTemplate.objects.create(
            **feed_template_dict)

        feed_template.save()
        feed_obj = Post.objects.create(
            user=validated_data['user'], feed_template=feed_template)
        feed_obj.save()
        return feed_template


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    profile__age = serializers.SerializerMethodField()

    def get_profile__age(self, obj):
        return obj.profile.get_age()

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name',
                  'email', 'profile__age', 'profile']
