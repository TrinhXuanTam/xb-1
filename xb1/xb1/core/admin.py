from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UserRegistrationForm, UserUpdateForm
from .models import User, Profile


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = UserRegistrationForm
    form = UserUpdateForm




admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)

from django.contrib import admin

# Register your models here.
