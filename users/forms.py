from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StaffProfile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Below form will allow us to update the email and username
class StaffUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


# Below form will allow us to update the profile image, although both will be showed as a single form.
class StaffProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ['image']