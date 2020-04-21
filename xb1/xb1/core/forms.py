from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User, Profile


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


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image', 'name', 'surname', 'city', 'postalCode', 'address', 'phone']
        help_texts = {
            'image': None,
            'name': None,
            'surname': None,
            'city': None,
            'postalCode': None,
            'address': None,
            'phone': None
        }
