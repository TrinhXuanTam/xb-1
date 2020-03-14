from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.views.generic import TemplateView
from django.urls import reverse_lazy


class IndexView(TemplateView):

    template_name = "index.html"


class LoginView(BaseLoginView):

    pass


class LogoutView(BaseLogoutView):

    next_page = reverse_lazy("login")