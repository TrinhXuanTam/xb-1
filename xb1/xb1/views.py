from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView, \
    PasswordResetConfirmView as AuthPasswordResetConfirmView, \
    PasswordResetCompleteView as AuthPasswordResetCompleteView, \
    PasswordResetView as AuthPasswordResetView, PasswordResetDoneView as AuthPasswordResetDoneView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils.translation import ugettext_lazy as _

from .core.tokens import account_activation_token
from .core.views import LoginMixinView
from django.views.generic.edit import FormView, UpdateView

from django.contrib.auth.views import PasswordChangeView as AuthPasswordChangeView

from .articles.models import Article, UploadedFile, Comment
from .core.forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm, UserChangeEmailForm, \
    ChangePasswordForm, ChangePasswordResetForm, PasswordResetEmailForm

from .core.models import User, Profile
from django.contrib.auth.forms import UserCreationForm

from django.http import JsonResponse, HttpResponseRedirect

# CKEDITOR
from ckeditor_uploader.views import browse, upload, get_files_browse_urls
from ckeditor_uploader.forms import SearchForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from .articles.models import UploadedFile
import json
import os

from .settings import EMAIL_HOST_USER

"""
Messages shown at login/logout
"""


def show_logout_message(sender, user, request, **kwargs):
    messages.info(request, 'Byl jste úspěšně odhlášen.')


def show_login_message(sender, user, request, **kwargs):
    messages.info(request, f'Vítejte {user.username}.')


user_logged_out.connect(show_logout_message)

user_logged_in.connect(show_login_message)


class IndexView(LoginMixinView, ListView):
    """
    View displays home page with latest article on front page
    """
    model = Article
    queryset = Article.objects.filter(article_state=1).order_by('-modified')
    template_name = "index.html"


class LoginViewModal(LoginMixinView, BaseLoginView):
    """
    View handles ajax requests from modal login view
    """
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


class LoginView(LoginMixinView, BaseLoginView):
    """
    Basic login view inherited from BaseLoginView
    """
    template_name = "registration/login.html"
    form_class = UserLoginForm


class LogoutView(BaseLogoutView):
    """
    Basic login view inherited from BaseLogoutView
    """
    pass


class ProfileView(LoginMixinView, LoginRequiredMixin, ListView):
    """
    Profile view for authenticated users, user can change his credentials and set his profile picture
    """
    model = User
    template_name = "profile.html"
    form_class = ProfileUpdateForm

    def get_context_data(self, *args, **kwargs):
        """
        Method fills in profile form with data of the authenticated user
        """
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        context["p_form"] = ProfileUpdateForm(instance=self.request.user.profile)
        return context

    def post(self, request, **kwargs):
        p_form = ProfileUpdateForm(self.request.POST, self.request.FILES, instance=self.request.user.profile)

        if p_form.is_valid():
            p_form.save()
            messages.success(self.request, f'Váš účet byl úspěšně zaktualizován.')
            return redirect('profile')


class ActivationSentView(LoginMixinView, ListView):
    """
    If user decides to change email from profile section and enters an email, this view displays sent message.
    """
    model = User
    template_name = "registration/activation_sent.html"


class PasswordChangeView(LoginMixinView, AuthPasswordChangeView):
    """
    View displays a form to change password
    """
    form_class = ChangePasswordForm
    success_url = '/profile/'
    template_name = "registration/password_change_form.html"


def activate_email(request, uidb64, token):
    """
    Function checks token sent during email change process,
    if tokens match then email change is finished, otherwise error message is shown
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        if User.objects.get(temp_email=user.temp_email) is not None:
            return render(request, 'registration/activation_email_unique_fail.html')

        user.email = user.temp_email
        user.temp_email = None
        user.save()
        login(request, user)
        messages.success(request, f'Aktualizace proběhla úspěšně.')
        return redirect('index')
    else:
        return render(request, 'registration/activation_invalid.html')


def activate_registration(request, uidb64, token):
    """
    Function checks token sent during registration process,
    if tokens match then registration is finished, otherwise error message is shown
    """
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


class EmailChangeView(LoginMixinView, LoginRequiredMixin, FormView):
    """
    View displays email change form and sends authentication link to entered email,
    newly entered email is saved in a temporary variable and if new email is valid
    then temporary email is set as email
    """
    template_name = 'registration/email_change.html'
    form_class = UserChangeEmailForm

    def form_valid(self, form):
        form = self.form_class(self.request.POST, instance=self.request.user)
        form.save()
        self.request.user.temp_email = form.cleaned_data['temp_email']
        self.request.user.save()
        current_site = get_current_site(self.request)
        subject = 'Potvrďte Váš nový email'
        # load a template like get_template()
        # and calls its render() method immediately.
        message = render_to_string('registration/activation_request_email.html', {
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(self.request.user.pk)),
            # method will generate a hash value with user related data
            'token': account_activation_token.make_token(self.request.user),
        })
        send_mail(subject, message, EMAIL_HOST_USER, [str(self.request.user.temp_email)], fail_silently=False)
        return redirect('activation_sent')


class PasswordResetView(LoginMixinView, AuthPasswordResetView):
    """
    View displays password reset form and sends reset password details to entered email
    """
    form_class = PasswordResetEmailForm
    template_name = "registration/password_reset.html"


class PasswordResetConfirmView(LoginMixinView, AuthPasswordResetConfirmView):
    """
    View displays password reset form and sends reset password details to entered email
    """
    form_class = ChangePasswordResetForm
    template_name = "registration/password_reset_confirm.html"


class PasswordResetDoneView(LoginMixinView, AuthPasswordResetDoneView):
    """
    View displays message that informs user that password has been sent
    """
    template_name = "registration/password_reset_done.html"


class PasswordResetCompleteView(LoginMixinView, AuthPasswordResetCompleteView):
    """
    View displays message that informs user that password has been changed
    """
    template_name = "registration/password_reset_complete.html"


class Register(LoginMixinView, FormView):
    """
    View displays registration form and sends activation token to entered email
    """
    template_name = "registration/register.html"
    form_class = UserRegistrationForm

    def form_valid(self, form):
        form = self.form_class(self.request.POST)
        user = form.save()
        current_site = get_current_site(self.request)
        subject = 'Potvrďte Váš email'
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


# CKEDITOR
class CKEditorUploadView(LoginRequiredMixin, View):
    """
    Saves a file uploaded via CKEditor.
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CKEditorUploadView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = upload(request, *args, **kwargs)
        if b"Invalid" not in response.content:
            location = json.loads(response.content)
            path = os.path.relpath(location['url'], '/media')
            UploadedFile(uploaded_file=path).save()
        return response


class CKEditorBrowseView(LoginRequiredMixin, View):
    """
    Renders a list of all uploaded files in the CKEditor file manager.
    """

    permission_required = "articles.change_article"

    def get(self, request, *args, **kwargs):
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


class CKEditorDeleteView(LoginRequiredMixin, View):
    """
    Deletes an existing file in CKEditor file manager.
    """

    def post(self, request, *args, **kwargs):
        src = request.POST.get('DeleteButton')
        res = UploadedFile.objects.filter(uploaded_file=os.path.relpath(src, '/media'))
        for x in res:
            x.delete()
        return HttpResponseRedirect("/ckeditor/browse")


class UserListView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, ListView):

    template_name = 'users/user_list.html'
    paginate_by = 10
    permission_required = "core.view_user"

    def get_queryset(self):
        keywords = self.request.GET.get('keywords')

        if not keywords:
            return User.objects.all().order_by("-pk")

        keywords = keywords.split()
        if keywords:
            return User.objects.filter(Q(profile__nickname__icontains=keywords[0]) | Q(username__icontains=keywords[0])).order_by("-pk")
        else:
            return User.objects.all().order_by("-pk")


class UserDetailView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = User
    template_name = "users/user_detail.html"
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("user_list")
    permission_required = "core.view_user"

    def get_context_data(self, *args, **kwargs):
        """
        Method fills in profile form with data of the authenticated user
        """
        context = super(UserDetailView, self).get_context_data(*args, **kwargs)
        context["form"] = ProfileUpdateForm(instance=self.object.profile)
        context["is_user_staff_member"] = self.object.has_perm("core.view_user")
        return context

    def post(self, request, **kwargs):

        if "update_user" in request.POST:
            p_form = ProfileUpdateForm(self.request.POST, self.request.FILES, instance=User.objects.get(pk=self.kwargs['pk']).profile)
            if p_form.is_valid():
                p_form.save()
                messages.success(request, _("User has successfuly updated."))

        elif "ban_user" in request.POST:
            user = User.objects.get(pk=self.kwargs['pk'])
            user.is_active = False
            user.save()
            messages.success(request, _("User has been banned"))

        elif "unban_user" in request.POST:
            user = User.objects.get(pk=self.kwargs['pk'])
            user.is_active = True
            user.save()
            messages.success(request, _("User's ban has been removed."))

        elif "set_user_as_staff" in request.POST:
            user = User.objects.get(pk=self.kwargs['pk'])
            group = Group.objects.get(pk=3)
            if group:
                user.groups.add(group)
                user.save()
                messages.success(request, _("User has been set as a staff member."))
            else:
                messages.error(request, _("User cannot be set as a staff member."))

        elif "remove_staff_group" in request.POST:
            user = User.objects.get(pk=self.kwargs['pk'])
            if user == self.request.user:
                messages.error(request, _("You cannot remove your permission."))
            else:
                group = Group.objects.get(pk=3)
                user.groups.remove(group)
                user.save()
                messages.success(request, _("Staff group was removed from the user."))

        return redirect('user_list')


class UserCommentsView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'users/user_comments.html'
    paginate_by = 5
    permission_required = "core.view_user"

    def get_queryset(self):
        return Comment.objects.filter(author__pk=self.kwargs['pk']).order_by("-pk")
