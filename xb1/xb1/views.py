from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from .core.forms import UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


class IndexView(TemplateView):
    template_name = "index.html"


class LoginView(BaseLoginView):
    pass


class LogoutView(BaseLogoutView):
    # next_page = reverse_lazy("login")
    pass


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


@login_required
def profile(request):
    return render(request, 'registration/profile.html')
