from django.contrib import admin
from user_profile.models import UserProfile, FeedTemplate, Post
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(FeedTemplate)
admin.site.register(Post)
