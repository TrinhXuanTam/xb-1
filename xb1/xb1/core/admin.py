from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UserRegistrationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = UserRegistrationForm
    form = CustomUserChangeForm


admin.site.register(User, CustomUserAdmin)
from django.contrib import admin

# Register your models here.
