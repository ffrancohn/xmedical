from django.contrib import admin

from .models import UserPreference


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ("user", "theme", "updated_at")
    search_fields = ("user__username", "user__first_name", "user__last_name")
