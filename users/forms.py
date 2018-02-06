from django import forms
from django.contrib.auth.models import User
from users.models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False)

    class Meta():
        model = UserProfile
        fields = ('picture',)


class CommonUserForm(UserForm, UserProfileForm):
    pass