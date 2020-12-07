from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UserRegistrationForm, UserUpdateForm
from .models import User, Profile, Log, Message


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = UserRegistrationForm
    form = UserUpdateForm

class CustomAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances (even the deleted ones), that can be edited by the
        admin site. This is used by changelist_view.
        """
        try:
            qs = self.model._default_manager.get_full_queryset()
        except:
            qs = self.model._default_manager.get_queryset()

        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
	list_display = ("user", "timestamp", "action", "article", "order", "comment", "forum")


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Message)
