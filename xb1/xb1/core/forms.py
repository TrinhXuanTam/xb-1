from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm, \
    SetPasswordForm, PasswordResetForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.forms import Textarea

from .models import User, Profile


# custom login form
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        # set text placeholders
        self.fields['username'].widget.attrs['placeholder'] = _("User name")
        self.fields['password'].widget.attrs['placeholder'] = _("Password")

        # set css class
        self.fields['username'].widget.attrs['class'] = 'login_input'
        self.fields['password'].widget.attrs['class'] = 'login_input'

        self.fields['username'].widget.attrs['autocomplete'] = 'off'
        self.fields['password'].widget.attrs['autocomplete'] = 'off'

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("Your account has been banned."),
                code='inactive',
            )

    def clean(self):
        try:
            User.objects.get(username__iexact=self.cleaned_data["username"])
        except User.DoesNotExist:
            raise ValidationError(_("Incorrect username"))

        if not authenticate(username=self.cleaned_data["username"], password=self.cleaned_data["password"]):
            raise ValidationError(_("Incorrect password"))

        cleaned_data = super(UserLoginForm, self).clean()
        return cleaned_data


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for field_name in ('username', 'email', 'password1', 'password2'):
            # remove helper text
            self.fields[field_name].help_text = None
            # remove labels
            self.fields[field_name].label = False

            self.fields[field_name].widget.attrs['class'] = 'registration_input'

        # set text placeholders
        self.fields['username'].widget.attrs['placeholder'] = _("User name")
        self.fields['email'].widget.attrs['placeholder'] = _("Email")
        self.fields['password1'].widget.attrs['placeholder'] = _("Password")
        self.fields['password2'].widget.attrs['placeholder'] = _("Confirm password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
        help_texts = {
            'username': None,
            'email': None,
        }


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for field_name in ('old_password', 'new_password1', 'new_password2'):
            # remove helper text
            self.fields[field_name].help_text = None
            # remove labels
            self.fields[field_name].label = False

            self.fields[field_name].widget.attrs['class'] = 'registration_input'

        self.fields['old_password'].widget.attrs['placeholder'] = _("Current password")
        self.fields['new_password1'].widget.attrs['placeholder'] = _("New password")
        self.fields['new_password2'].widget.attrs['placeholder'] = _("New password confirmation")


    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


class ChangePasswordResetForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordResetForm, self).__init__(*args, **kwargs)
        for field_name in ('new_password1', 'new_password2'):
            # remove helper text
            self.fields[field_name].help_text = None
            # remove labels
            self.fields[field_name].label = False

            self.fields[field_name].widget.attrs['class'] = 'registration_input'

        self.fields['new_password1'].widget.attrs['placeholder'] = _("New pasword")
        self.fields['new_password2'].widget.attrs['placeholder'] = _("New password confirmation")

    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']


class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(required=False, error_messages={'invalid': _("Invalid file")},
                             widget=forms.FileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ('image', 'nickname', 'name', 'surname', 'city', 'postalCode', 'address', 'phone'):
            # remove helper text
            self.fields[field_name].help_text = None

            self.fields[field_name].widget.attrs['class'] = 'profile_input'

        self.fields['image'].label = _("Image")
        self.fields['nickname'].label = _("Nickname")
        self.fields['name'].label = _("Name")
        self.fields['surname'].label = _("Surname")
        self.fields['city'].label = _("City")
        self.fields['postalCode'].label = _("Postal code")
        self.fields['address'].label = _("Address")
        self.fields['phone'].label = _("Phone number")

    class Meta:
        model = Profile
        fields = ['nickname', 'name', 'surname', 'city', 'postalCode', 'address', 'phone', 'image']


class UserChangeEmailForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['temp_email'].widget.attrs['placeholder'] = _("New email")
        self.fields['temp_email'].label = False
        self.fields['temp_email'].widget.attrs['class'] = 'registration_input'

    def clean_temp_email(self):
        # Get the email
        temp_email = self.cleaned_data.get('temp_email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=temp_email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return temp_email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError(_("This email has alredy been registered."))

    class Meta:
        model = User
        fields = ['temp_email']


class PasswordResetEmailForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = _("Enter your email")
        self.fields['email'].label = False
        self.fields['email'].widget.attrs['class'] = 'registration_input'

    class Meta:
        model = User
        fields = ['email']
