from django import forms
from django.contrib.auth import authenticate, get_user_model

from devtools.decorators import class_logging

User = get_user_model()


class LoginForm(forms.Form):
    email_attributes = {
        'class': 'form-control',
        'type': 'email',
        'placeholder': 'Enter email',
        'id': 'login-email-input'
    }

    password_attributes = {
        'class': 'form-control',
        'type': 'password',
        'placeholder': 'Enter password',
        'id': 'login-password-input'
    }

    email = forms.EmailField(widget=forms.EmailInput(attrs=email_attributes))
    password = forms.CharField(widget=forms.PasswordInput(attrs=password_attributes))

    model = User

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


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'phone_number', 'email', 'password']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Enter your name',
                'id': 'register-name-input'
            }),
            'surname': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Enter your surname',
                'id': 'register-surname-input'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Enter your number',
                'id': 'register-phone-number-input'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'type': 'email',
                'placeholder': 'Enter your email address',
                'id': 'register-email-input'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'type': 'password',
                'placeholder': 'Enter password',
                'id': 'register-password-input'
            })
        }

    password_confirmation = forms.CharField(widget=forms.PasswordInput(attrs={
                'class': 'form-control',
                'type': 'password',
                'placeholder': 'Enter password',
                'id': 'register-password-confirmation-input'
            }))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already taken!')
        return email

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) == 0:
            raise forms.ValidationError('Name can\'t be empty!')
        return name

    def clean_surname(self):
        surname = self.cleaned_data.get('surname')
        if len(surname) == 0:
            raise forms.ValidationError('Surname can\'t be empty!')
        return surname

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(phone_number) == 0:
            raise forms.ValidationError('Phone number can\'t be empty!')
        if not phone_number.isdigit():
            raise forms.ValidationError('Incorrect phone number format! Only digits acceptable!')
        return phone_number

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password too short. Enter at least 8 symbols!')
        return password

    def clean(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            raise forms.ValidationError({'password_confirmation': 'Passwords do not match!'})
        return self.cleaned_data

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        self.instance.name = cleaned_data.get('name')
        self.instance.surname = cleaned_data.get('surname')
        self.instance.email = cleaned_data.get('email')
        self.instance.phone_number = cleaned_data.get('phone_number')
        self.instance.set_password(cleaned_data.get('password'))
        self.instance.is_active = False
        self.instance.is_staff = False
        self.instance.is_admin = False
        super().save(commit)
