import code
from functools import reduce

from django.db.models import Q
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


from .models import (
    Product,
    Category,
    Image,
)
from .forms import ExposeProductForm


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
    template_name = 'products/productdetail.html'

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.queryset
        id = self.kwargs.get('id')
        try:
            item = queryset.get(id=id)
        except self.model.DoesNotExist as ex:
            raise Http404()
        return item


class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.all()
    template_name = 'products/categories.html'


class CategoryFilterProductView(ListView):
    model = Product
    queryset = None
    template_name = 'products/productslist.html'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=None, **kwargs)

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug == 'all':
            queryset = self.model.objects.all()
        else:
            queryset = self.model.objects.filter(category__slug=category_slug)
        search = self.kwargs.get('search')
        if search:
            search_args = search.split()
            query_params = [Q(item) for item in search_args]
            query = reduce(lambda total, item: total | item, query_params)
            queryset = queryset.filter(query).distinct()
        return queryset


def handle_files(files, product):
    images = files.getlist('images')
    for image in images:
        Image(image=image, product=product).save()


class ExposeProductView(LoginRequiredMixin, FormView):
    form_class = ExposeProductForm
    template_name = 'products/exposeproduct.html'

    def handle_no_permission(self):
        return redirect(reverse_lazy('accounts:login') + '?next={}'.format(self.request.path))

    def get_form(self, form_class=None):
        return self.form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        print('# valid')
        print('#', self.request.FILES)
        product = form.save()
        handle_files(self.request.FILES, product)
        return redirect(form.product.get_absolute_url())

    def form_invalid(self, form):
        return super().form_invalid(form)
