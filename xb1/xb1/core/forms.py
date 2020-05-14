from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm, \
    SetPasswordForm, PasswordResetForm
from .models import User, Profile
from django.forms import Textarea


# custom login form
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        # set text placeholders
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

        # set css class
        self.fields['username'].widget.attrs['class'] = 'login_input'
        self.fields['password'].widget.attrs['class'] = 'login_input'

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "This account is inactive.",
                code='inactive',
            )


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
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Retype password'

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

        self.fields['old_password'].widget.attrs['placeholder'] = 'Současné heslo'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Nové heslo'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Potvrdit heslo'


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

        self.fields['new_password1'].widget.attrs['placeholder'] = 'Nové heslo'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Potvrdit heslo'

    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']


class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(required=True, error_messages={'invalid': "Neplatný soubor."},
                             widget=forms.FileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ('image', 'nickname', 'name', 'surname', 'city', 'postalCode', 'address', 'phone'):
            # remove helper text
            self.fields[field_name].help_text = None

            self.fields[field_name].widget.attrs['class'] = 'profile_input'

        self.fields['image'].label = 'Obrázek'
        self.fields['nickname'].label = 'Přezdívka'
        self.fields['name'].label = 'Jméno'
        self.fields['surname'].label = 'Příjmení'
        self.fields['city'].label = 'Město'
        self.fields['postalCode'].label = 'PSČ'
        self.fields['address'].label = 'Adresa'
        self.fields['phone'].label = 'Telefonní číslo'

    class Meta:
        model = Profile
        fields = ['image', 'nickname', 'name', 'surname', 'city', 'postalCode', 'address', 'phone']


class UserChangeEmailForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['temp_email'].widget.attrs['placeholder'] = 'Nový email'
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
        raise forms.ValidationError('Tento email je používán.')

    class Meta:
        model = User
        fields = ['temp_email']


class PasswordResetEmailForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Zadejte váš email'
        self.fields['email'].label = False
        self.fields['email'].widget.attrs['class'] = 'registration_input'

    class Meta:
        model = User
        fields = ['email']

