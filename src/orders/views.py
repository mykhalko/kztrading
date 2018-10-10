from functools import reduce

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import ListView, View
from django.shortcuts import render

from products.models import Product
from .models import Order


@login_required
class OrdersView(ListView):
    template_name = 'orders/defaultorders.html'
    model = Order

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(buyer=user)
        return queryset


@login_required
class ConfirmOrders(View):
    template_name = 'orders/defaultorders.html'

    def get_queryset(self):
        items = self.request.session.get('cart_items')
        if not items:
            return None
        queryset = Product.objects.filter_id(items)
        return queryset

    def get_context_data(self):
        queryset = self.get_queryset()
        self.queryset = queryset
        return {
            'object_list': queryset
        }

    def get(self, *args, **kwargs):
        pass