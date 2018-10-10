from functools import reduce

from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView

from products.models import Product


class CartItemsView(ListView):
    template_name = 'cart/defaultcart.html'

    def get_queryset(self):
        items = self.request.session.get('cart_items')
        if not items:
            return None
        queryset = Product.objects.filter_id(items)
        return queryset
