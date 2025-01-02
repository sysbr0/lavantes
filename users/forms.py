# forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from .models import CustomUser

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Set the username to be the same as the email
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Invalid email or password')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('This account is inactive.')
        return self.cleaned_data




from django.contrib.auth.forms import AuthenticationForm

class LogingForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))