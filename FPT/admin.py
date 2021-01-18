from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .models import *
# Register your models here.
admin.site.register(Trainee)
admin.site.register(Trainer)
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Request)


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (
            "User",
            {
                "fields": (
                    "is_trainer",
                    "is_trainee",
                )
            },
        ),
    ) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "is_superuser", "is_staff", "is_trainer", "is_trainee"]
