from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, DetailView
from django.shortcuts import render, redirect
from django.http import Http404


from . import forms
from .models import Confirmation


class LoginView(UserPassesTestMixin ,FormView):
    template_name = 'accounts/login.html'
    form_class = forms.LoginForm

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('/')

    def get_form(self, form_view = None):
        return self.form_class(request=self.request, **self.get_form_kwargs())

    def get_success_url(self):
        return 'accounts/login_success'

    def form_valid(self, form):
        login(request=self.request, user=form.user)
        return redirect('/')

    def form_invalid(self, form):
        context = self.get_context_data()
        context.update({
            'form': form,
            'login_failed_message': 'Incorrect email or password'
            })
        return self.render_to_response(context)
        # return super().form_invalid(form)


class RegisterView(UserPassesTestMixin, FormView):
    template_name = 'accounts/registration.html'
    form_class = forms.RegistrationForm

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('/')

    def get_success_url(self):
        return 'accounts/register_success'

    def form_valid(self, form):
        form.save()
        user = form.instance
        confirmation = Confirmation.objects.create_confirmation_link(user)
        self.send_confirmation(confirmation)
        # return redirect('/accounts/registration_success/')
        return render(self.request, 'accounts/registration_success.html', {})

    def form_invalid(self, form):
        context = self.get_context_data()
        context.update({
            'form': form,
            'registration_failed_message': form.errors
        })
        return self.render_to_response(context)

    def send_confirmation(self, confirmation):
        request = self.request
        subject = 'Please verify your email address'
        link = ''.join(['http://', request.get_host(), '/accounts/confirm/', str(confirmation.id)])
        message_raw = \
            'Hi! Thank you for getting started with kztrading.\n' \
            'We need a little bit more information to complete your registration.' \
            'Click link below to confirm your email address.\n\n{}\n\n' \
            'Didn’t request this email?\nNo worries! Your address may have been ' \
            'entered by mistake. If you ignore or delete this email, nothing further ' \
            'will happen.'
        message = message_raw.format(link)
        mail = EmailMessage(subject, message, to=[confirmation.user.email])
        mail.send()


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


class ConfirmView(DetailView):
    template_name = 'accounts/confirm.html'
    model = Confirmation

    object = None
    slug_field = 'id'
    slug_url_kwarg = 'uuid_key'

    def get_object(self, queryset=None):
        try:
            obj = self.model.objects.get(id=self.kwargs.get(self.slug_url_kwarg))
            self.object = obj
        except self.model.DoesNotExist as ex:
            raise Http404()
        except ValidationError as ex:
            raise Http404()
        return obj

    def get_context_data(self, **kwargs):
        email = self.object.user.email
        return {'email': email}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.visited is True:
            raise Http404()
        self.object.visited = True
        self.object.user.is_active = True
        self.object.user.save()
        self.object.save()
        context = self.get_context_data()
        return self.render_to_response(context)

