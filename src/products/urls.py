from django.conf.urls import url

from . import views


app_name = 'products'


urlpatterns = [
    url('items/(?P<id>[0-9]+)/$', views.ProductDetailView.as_view(), name='item'),
    url('items/', views.ProductsView.as_view(), name='items'),
]
