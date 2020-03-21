from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.signals import user_logged_out, user_logged_in


from .articles.models import Animal, Article
from .core.forms import UserRegistrationForm
from .core.models import User


def show_logout_message(sender, user, request, **kwargs):
    messages.info(request, 'You have been logged out.')


def show_login_message(sender, user, request, **kwargs):
    messages.info(request, f'Welcome {user.username}')


user_logged_out.connect(show_logout_message)

user_logged_in.connect(show_login_message)


class IndexView(ListView):
    model = Article
    template_name = "index.html"


class LoginView(BaseLoginView):
    pass


class LogoutView(BaseLogoutView):
    pass


class ProfileView(ListView):
    model = User
    template_name = "profile.html"


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})





