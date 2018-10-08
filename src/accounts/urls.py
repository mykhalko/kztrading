from django.conf.urls import url

from . import views


app_name = 'accounts'


urlpatterns = [
    url('login/$', views.LoginView.as_view(), name='login'),
    url('register/$', views.RegisterView.as_view(), name='register'),
    url('confirm/(?P<uuid_key>[0-9a-zA-Z-]+)/$', views.ConfirmView.as_view()),
    # url('registration_success/$', views.registration_success_view),
    url('logout/$', views.logout_view, name='logout'),
]
