from django.contrib import admin

from core.models import Profile, UserProfile, Game

# Register your models here.
admin.site.register(Profile)
admin.site.register(UserProfile)
admin.site.register(Game)