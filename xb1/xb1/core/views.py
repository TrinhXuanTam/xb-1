from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import translation
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.views.generic import View, RedirectView

from .forms import UserLoginForm
from .. import settings


class LoginMixinView(View):
    """
    Adds login form to context data.
    (Every site, which has login form must inherit this view)
    """

    def get_context_data(self, *args, **kwargs):

        context = super(LoginMixinView, self).get_context_data(*args, **kwargs)

        context["login_form"] = UserLoginForm

        return context


class SwitchLanguageRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):

        if hasattr(self.request, "session"):
            session_language = self.request.session.get(LANGUAGE_SESSION_KEY, None)

            if session_language == "en":
                self.request.session[LANGUAGE_SESSION_KEY] = "cs"
            else:
                self.request.session[LANGUAGE_SESSION_KEY] = "en"
            self.request.session.save()

            translation.activate(self.request.session[LANGUAGE_SESSION_KEY])

        print(self.request.session[LANGUAGE_SESSION_KEY])

        return reverse_lazy("index")
