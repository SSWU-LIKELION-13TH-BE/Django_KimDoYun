from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['nickname','email','username', 'password1', 'password2']

User = get_user_model()

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['nickname', 'username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']
