from django.views.generic import FormView
from django.shortcuts import render, redirect

from . import forms


class LoginView(FormView):
    template_name = 'accounts/default.html'
    form_class = forms.LoginForm

    def get_form(self, form_view = None):
        return self.form_class(request=self.request, **self.get_form_kwargs())

    def get_success_url(self):
        return 'accounts/login_success'

    def form_valid(self, form):
        print('# form valid')
        return super().form_valid(form)

    def form_invalid(self, form):
        print('# form invalid')
        return super().form_invalid(form)


class RegisterView(FormView):
    template_name = 'accounts/default.html'
    form_class = forms.RegistrationForm

    def get_success_url(self):
        return 'accounts/register_success'

    def form_valid(self, form):
        print('# form valid')
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print('# form invalid')
        return  super().form_invalid(form)
