import code
from functools import reduce

from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Product


class ProductsView(ListView):
    model = Product
    template_name = 'products/defaultlist.html'

    def get_queryset(self):
        category_title = self.kwargs.get('category')
        if category_title:
            queryset = self.model.objects.category(category_title)
        else:
            queryset = self.model.objects.all()
        if self.kwargs.get('search'):
            search_args = self.kwargs.get('search').split()
            query_list = [Q(title__icontains=item) for item in search_args]
            query = reduce(lambda total, item: total | item, query_list)
            queryset = queryset.filter(query).distinct()
        return queryset

    def get(self, *args, **kwargs):
        self.kwargs.update({key: value for key, value in self.request.GET.items()})
        print(self.kwargs)
        result = super().get(*args, **kwargs)
        return result


class ProductDetailView(DetailView):
    model = Product
    queryset = Product.objects
    template_name = 'products/defaultdetail.html'

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.queryset
        id = self.kwargs.get('id')
        try:
            item = queryset.get(id=id)
        except self.model.DoesNotExist as ex:
            raise Http404()
        return item


