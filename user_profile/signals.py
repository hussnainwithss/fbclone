from django.db.models.signals import post_save
from django.dispatch import receiver
from user_profile.models import UserProfile, FeedTemplate, Post
from accounts.views import user_profile_create_signal


@receiver(post_save, sender=UserProfile)
def create_registration_post(sender, instance, created, **kwargs):
    if created:
        feed_template = FeedTemplate.objects.create(
            feed_type='register', content='{} has joined UBook'.format(instance.user.first_name))
        feed_obj = Post.objects.create(
            user=instance.user, feed_template=feed_template)


@receiver(user_profile_create_signal)
def create_user_profile(**kwargs):
    if kwargs['user']:
        UserProfile.objects.create(user=kwargs['user'], gender=kwargs.get(
            'gender'), birthday=kwargs.get('birthday'))
