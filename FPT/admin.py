from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
# Register your models here.
admin.site.register(Trainee)
admin.site.register(User, UserAdmin)
admin.site.register(Trainer)
admin.site.register(Course)
admin.site.register(Category)
