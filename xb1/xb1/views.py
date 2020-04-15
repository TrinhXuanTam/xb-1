from django.contrib.auth import login
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.signals import user_logged_out, user_logged_in

from .core.tokens import account_activation_token
from .core.views import LoginMixinView
from django.views.generic.edit import FormView


from .articles.models import Article
from .core.forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm, UserUpdateForm
from .core.models import User, Profile
from django.contrib.auth.forms import UserCreationForm

from django.http import JsonResponse

def show_logout_message(sender, user, request, **kwargs):
    messages.info(request, 'You have been logged out.')


def show_login_message(sender, user, request, **kwargs):
    messages.info(request, f'Welcome {user.username}')


user_logged_out.connect(show_logout_message)

user_logged_in.connect(show_login_message)


class IndexView(LoginMixinView, ListView):
    model = Article
    template_name = "index.html"


class LoginView(LoginMixinView, BaseLoginView):
    template_name = "registration/login.html"
    form_class = UserLoginForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        response = JsonResponse({"ok": "login success"})
        response.status_code = 200
        return response

    def form_invalid(self, form):
        response = JsonResponse({"error": "login failed"})
        response.status_code = 401
        return response


class LogoutView(BaseLogoutView):
    pass


class ProfileView(LoginMixinView, ListView):
    model = User
    template_name = "profile.html"
    form_class = ProfileUpdateForm

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        context["p_form"] = ProfileUpdateForm(instance=self.request.user.profile)
        return context

    def post(self, request, **kwargs):
        p_form = ProfileUpdateForm(self.request.POST, self.request.FILES, instance=self.request.user.profile)

        if p_form.is_valid():
            p_form.save()
            messages.success(self.request, f'Your account has been updated!')
            return redirect('profile')
        # username = form.cleaned_data.get('username')
        # messages.success(self.request, f'Account created for {username}! You can now log in.')
        # return redirect('login')



class ActivationSentView(LoginMixinView, ListView):
    model = User
    template_name = "registration/activation_sent.html"


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        user.is_active = True
        # set signup_confirmation true
        user.signup_confirmation = True
        user.save()
        profile = Profile(user=user)
        profile.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'registration/activation_invalid.html')


class Register(LoginMixinView, FormView):
    template_name = "registration/register.html"
    form_class = UserRegistrationForm

    def form_valid(self, form):
        form = self.form_class(self.request.POST)
        user = form.save()
        current_site = get_current_site(self.request)
        subject = 'Please Activate Your Account'
        user.is_active = False
        user.signup_confirmation = False
        user.save()
        # load a template like get_template()
        # and calls its render() method immediately.
        message = render_to_string('registration/activation_request.html', {
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            # method will generate a hash value with user related data
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)
        return redirect('activation_sent')
        # username = form.cleaned_data.get('username')
        # messages.success(self.request, f'Account created for {username}! You can now log in.')
        # return redirect('login')


# def register(request):
#    if request.method == 'POST':
#       form = UserRegistrationForm(request.POST)
#        if form.is_valid():
#            form.save()
#            username = form.cleaned_data.get('username')
#            messages.success(request, f'Account created for {username}! You can now log in.')
#            return redirect('login')
#    else:
#        form = UserRegistrationForm()
#    return render(request, 'registration/register.html', {'form': form})
