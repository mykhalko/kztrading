from django import forms
from django.contrib.auth import authenticate, get_user_model

from devtools.decorators import class_logging


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    model = get_user_model()

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(request=self.request, email=email, password=password)
        if not user:
            raise forms.ValidationError('Incorrect email or password')
        self.user = user
