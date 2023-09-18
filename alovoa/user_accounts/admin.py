# myapp/admin.py (replace 'myapp' with your app's name)

from django.contrib import admin
from .models import CustomUser, Profile, Preference, Image, UserLike, Subscription

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'profile_for', 'date_of_birth', 'religion', 'community', 'living_in', 'mobile_number', 'is_staff')
    list_filter = ('profile_for', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)


admin.site.register(Profile),
admin.site.register(Preference),
admin.site.register(Image),
admin.site.register(UserLike),
admin.site.register(Subscription)