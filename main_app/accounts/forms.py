from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate

from .models import CustomUser
from content.models import ContentUserProfile, Category

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


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "w-full py-2 input-border focus:border-green-400 text-gray-700" }),
        label="Email"
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "w-full py-2 input-border focus:border-green-400 text-gray-700"}),
        label="First Name"
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "w-full py-2 input-border focus:border-green-400 text-gray-700"}),
        label="Last Name"
    )
    stage = forms.ChoiceField(
        choices=ContentUserProfile.STAGE_CHOICES,
        widget=forms.Select(attrs={"class": "w-full py-2 input-border focus:border-green-400 text-gray-700 pr-8"}),
        label="Education Stage"
    )

    favorite_subject = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={"class": "w-full py-2 input-border focus:border-green-400 text-gray-700 pr-8"}),
        label="Favorite Subject"
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "w-full py-2 input-border focus:border-green-400 text-gray-700"})
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "w-full py-2 input-border focus:border-green-400 text-gray-700"})
    )

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "password1", "password2", "stage", "favorite_subject")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]


        if commit:
            user.save()
            ContentUserProfile.objects.create(
                user=user,
                stage=self.cleaned_data["stage"],
                favorite_subject=self.cleaned_data["favorite_subject"]
            )
        return user