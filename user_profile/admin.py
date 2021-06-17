from django.contrib import admin
from .models import UserProfile,FeedTemplate,Feed
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(FeedTemplate)
admin.site.register(Feed)
