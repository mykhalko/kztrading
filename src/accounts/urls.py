from django.conf.urls import url

from . import views

urlpatterns = [
    url('login/$', views.LoginView.as_view()),
    url('register/$', views.RegisterView.as_view()),
    url('confirm/(?P<uuid_key>[0-9a-zA-Z-]+)/$', views.ConfirmView.as_view())
]
