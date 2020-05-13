from django.contrib.auth import login
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView, \
    PasswordResetConfirmView as AuthPasswordResetConfirmView, PasswordResetCompleteView as AuthPasswordResetCompleteView, \
    PasswordResetView as AuthPasswordResetView, PasswordResetDoneView as AuthPasswordResetDoneView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
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

from django.contrib.auth.views import PasswordChangeView as AuthPasswordChangeView

from .articles.models import Article, UploadedFile
from .core.forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm, UserChangeEmailForm, \
    ChangePasswordForm, ChangePasswordResetForm, PasswordResetEmailForm

from .core.models import User, Profile
from django.contrib.auth.forms import UserCreationForm

from django.http import JsonResponse, HttpResponseRedirect

#CKEDITOR
from ckeditor_uploader.views import browse, upload, get_files_browse_urls
from ckeditor_uploader.forms import SearchForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .articles.models import UploadedFile
import json
import os

from .settings import EMAIL_HOST_USER


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


class PasswordChangeView(LoginMixinView, AuthPasswordChangeView):
    form_class = ChangePasswordForm
    success_url = '/profile/'
    template_name = "registration/password_change_form.html"


def activate_email(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        user.email = user.temp_email
        user.temp_email = None
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'registration/activation_invalid.html')


def activate_registration(request, uidb64, token):
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
        profile.nickname = user.username
        profile.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'registration/activation_invalid.html')


class EmailChangeView(LoginMixinView, FormView):
    template_name = 'registration/email_change.html'
    form_class = UserChangeEmailForm

    def form_valid(self, form):
        form = self.form_class(self.request.POST, instance=self.request.user)
        form.save()
        self.request.user.temp_email = form.cleaned_data['temp_email']
        self.request.user.save()
        current_site = get_current_site(self.request)
        subject = 'Please confirm your new email'
        # load a template like get_template()
        # and calls its render() method immediately.
        message = render_to_string('registration/activation_request_email.html', {
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(self.request.user.pk)),
            # method will generate a hash value with user related data
            'token': account_activation_token.make_token(self.request.user),
        })
        # self.request.user.email_user(subject, message)
        send_mail(subject, message, EMAIL_HOST_USER, [str(self.request.user.temp_email)], fail_silently=False)
        return redirect('activation_sent')


class PasswordResetView(LoginMixinView, AuthPasswordResetView):
    form_class = PasswordResetEmailForm
    template_name = "registration/password_reset.html"


class PasswordResetConfirmView(LoginMixinView, AuthPasswordResetConfirmView):
    form_class = ChangePasswordResetForm
    template_name = "registration/password_reset_confirm.html"


class PasswordResetDoneView(LoginMixinView, AuthPasswordResetDoneView):
    template_name = "registration/password_reset_done.html"


class PasswordResetCompleteView(LoginMixinView, AuthPasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"


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
        message = render_to_string('registration/activation_request_register.html', {
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

#CKEDITOR
@csrf_exempt
def ckeditor_upload(request, *args, **kwargs):
    response = upload(request, *args, **kwargs)
    if b"Invalid" not in response.content:
        location = json.loads(response.content)
        path = os.path.relpath(location['url'], '/media')
        UploadedFile(uploaded_file=path).save()
    return response

@csrf_exempt
def ckeditor_browse(request):
    files = get_files_browse_urls(request.user)
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data.get('q', '').lower()
            files = list(filter(lambda d: query in d[
                'visible_filename'].lower(), files))
    else:
        form = SearchForm()

    show_dirs = getattr(settings, 'CKEDITOR_BROWSE_SHOW_DIRS', False)
    dir_list = sorted(set(os.path.dirname(f['src'])
                          for f in files), reverse=True)

    if os.name == 'nt':
        files = [f for f in files if os.path.basename(f['src']) != 'Thumbs.db']

    context = {
        'show_dirs': show_dirs,
        'dirs': dir_list,
        'files': files,
        'form': form
    }
    return render(request, 'ckeditor_browse.html', context)

def ckeditor_delete(request):
    src = request.POST.get('DeleteButton')
    res = UploadedFile.objects.filter(uploaded_file=os.path.relpath(src, '/media'))
    for x in res:
        x.delete()
    return HttpResponseRedirect("/ckeditor/browse")