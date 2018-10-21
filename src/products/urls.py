from django.conf.urls import url

from . import views


app_name = 'products'



urlpatterns = [
    url('expose/$', views.ExposeProductView.as_view(), name='expose'),
    url('categories/$', views.CategoryListView.as_view(), name='categories'),
    url('items/(?P<id>[0-9]+)/$', views.ProductDetailView.as_view(), name='item'),
    url('items/', views.ProductsView.as_view(), name='items'),
    url('(?P<category>[a-zA-Z_]{1,128})/(?P<id>[0-9]+)/$',
        views.ProductDetailView.as_view(), name='category_item'),
    url('(?P<category_slug>[a-zA-Z_]{1,128})/', views.CategoryFilterProductView.as_view(), name='category'),
]
