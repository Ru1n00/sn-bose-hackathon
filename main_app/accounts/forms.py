from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

class UserAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "w-full py-2 input-border focus:border-green-400 text-white bg-slate-900", "placeholder": "Enter your email address"}),
        label="Email"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "w-full py-2 input-border focus:border-green-400 text-white bg-slate-900 pr-8", "placeholder": "Enter your password"}),
        label="Password"
    )

    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if email and password:
            return self.cleaned_data
        else:
            raise forms.ValidationError("Please enter both email and password.")
