from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.signals import user_logged_out, user_logged_in
from .core.views import LoginMixinView
from django.views.generic.edit import FormView



from .articles.models import Animal, Article
from .core.forms import UserRegistrationForm
from .core.models import User
from django.contrib.auth.forms import UserCreationForm


def show_logout_message(sender, user, request, **kwargs):
    messages.info(request, 'You have been logged out.')


def show_login_message(sender, user, request, **kwargs):
    messages.info(request, f'Welcome {user.username}')


user_logged_out.connect(show_logout_message)

user_logged_in.connect(show_login_message)


class IndexView(LoginMixinView, ListView):
    model = Article
    template_name = "index.html"


class LoginView(BaseLoginView):
    pass


class LogoutView(BaseLogoutView):
    pass


class ProfileView(LoginMixinView, ListView):
    model = User
    template_name = "profile.html"


class Register(LoginMixinView, FormView):
    template_name = "registration/register.html"
    form_class = UserRegistrationForm

    def form_valid(self, form):
        form = self.form_class(self.request.POST)
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Account created for {username}! You can now log in.')
        return redirect('login')


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
