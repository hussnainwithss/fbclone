from django.db.models.signals import post_save
from django.dispatch import receiver
from user_profile.models import UserProfile, FeedTemplate, Feed


@receiver(post_save, sender=UserProfile)
def create_registration_post(sender, instance, created, **kwargs):
    if created:
        feed_template = FeedTemplate.objects.create(
            feed_type='register', content='{} has joined UBook'.format(instance.user.first_name))
        feed_template.save()
        feed_obj = Feed.objects.create(
            user=instance.user, feed_template=feed_template)
        feed_obj.save()
