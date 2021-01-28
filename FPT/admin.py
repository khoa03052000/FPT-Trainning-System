from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .models import *
# Register your models here.
admin.site.register(Trainer)


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (
            "User",
            {
                "fields": (
                    "is_trainer",
                    "avatar",
                    "full_name",
                )
            },
        ),
    ) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "full_name", "is_superuser", "is_staff", "is_trainer", "is_trainee"]
