from django.conf.urls import url

from . import views, ajaxviews


app_name = 'cart'


urlpatterns = [
    url('add/$', ajaxviews.add_to_cart, name='add_to_cart'),
    url('remove/$', ajaxviews.RemoveView.as_view(), name='remove'),
    url('$', views.CartItemsView.as_view(), name='cart_items'),
    # ajax
    # url('ajax/items/$', ajaxviews.get_cart_items),
]
