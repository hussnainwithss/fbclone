from django.apps import AppConfig


class UserProfileConfig(AppConfig):
    name = 'user_profile'

    def ready(self):
        from user_profile.signals import create_registration_post, create_user_profile
