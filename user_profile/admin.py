from django.contrib import admin
from .models import Work,Education,UserProfile,City,Organization
# Register your models here.

admin.site.register(Work)
admin.site.register(Education)
admin.site.register(UserProfile)
admin.site.register(City)
admin.site.register(Organization)
