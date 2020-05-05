from django.shortcuts import render
from django.views.generic import View
from .forms import UserLoginForm

class LoginMixinView(View):

    def get_context_data(self, *args, **kwargs):

        context = super(LoginMixinView, self).get_context_data(*args, **kwargs)

        context["login_form"] = UserLoginForm

        return context
