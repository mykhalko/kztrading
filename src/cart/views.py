from functools import reduce

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import ListView

from products.models import Product


class CartItemsView(LoginRequiredMixin, ListView):
    template_name = 'cart/cart.html'

    def handle_no_permission(self):
        return redirect(reverse_lazy('accounts:login') + '?next={}'.format(self.request.path))

    def get_queryset(self):
        items = self.request.session.get('cart_items')
        if not items:
            return None
        queryset = Product.objects.filter_id(items)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        object_list = object_list if object_list else self.object_list
        if object_list:
            total_cost = reduce(lambda total, current: total + current.price, object_list, 0)
            context['total_cost'] = total_cost
        return context

