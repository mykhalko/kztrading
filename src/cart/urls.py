from django.conf.urls import url

from . import views, ajaxviews


app_name = 'cart'


urlpatterns = [
    url('items/$', views.CartItemsView.as_view(), name='cart'),
    # ajax
    url('ajax/items/$', ajaxviews.get_cart_items),
    url('ajax/add_to_cart/$', ajaxviews.add_to_cart)
]
