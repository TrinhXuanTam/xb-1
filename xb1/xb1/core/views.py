from django.shortcuts import render
from django.views.generic import View
from .forms import UserLoginForm


class LoginMixinView(View):

    def get_context_data(self, *args, **kwargs):

        context = super(LoginMixinView, self).get_context_data(*args, **kwargs)

        context["login_form"] = UserLoginForm

        return context


#   <form method = "POST" action = "{% url 'login' %}?next={{ request.path }}">
#     {% csrf_token %}
#     <h1>{{ login_form.username }}</h1>
#     <h1>{{ login_form.password }}</h1>
#     <br>
#     <button type = "submit">Login</button>
#   </form>
