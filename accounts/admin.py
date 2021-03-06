from django.contrib import admin
from django.contrib.auth import get_user_model
from accounts.models import OTP

USER = get_user_model()


@admin.register(USER)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_verify', 'is_staff', 'is_superuser']


admin.site.register(OTP)
