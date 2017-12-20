"""Module contain form classes for django based facade"""
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm


class SimpleLoginForm(forms.Form):
    """Simple login form implementation"""
    email = forms.EmailField(
        label="E-Mail",
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )


class RegistrationForm(UserCreationForm):
    """User register form based on django UserCreationForm"""
    class Meta:
        model = User
        fields = ("email",)
        field_classes = {"email": forms.EmailField}

    def clean_email(self):
        email = self.cleaned_data["email"]
        # django base form does not check, that user already exists :(
        exists = User.objects.filter(email=email)  # Quick and dirty hack
        if exists:
            raise forms.ValidationError("Given email already registered")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('email')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2
