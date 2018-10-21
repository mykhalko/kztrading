from django import forms

from .models import (
    Category,
    Product,
    Image
)


class ExposeProductForm(forms.Form):
    class FieldsAttrs:
        title = {
            'id': 'expose-product-title-id',
            'class': 'form-control'
        }
        price = {
            'id': 'expose-product-price-id',
            'class': 'form-control'
        }
        description = {
            'id': 'expose-product-description-id',
            'class': 'form-control',
            'style': 'resize: none'
        }
        # images = {
        #     'id': 'expose-product-images-id',
        #     'multiple': True,
        #     'class': 'custom-file-input'
        # }
        category = {
            'id': 'expose-product-category-id',
            'class': 'form-control'
        }

    title = forms.CharField(required=True,
                            widget=forms.TextInput(attrs=FieldsAttrs.title))
    price = forms.DecimalField(decimal_places=2, max_digits=10, required=True,
                               widget=forms.NumberInput(attrs=FieldsAttrs.price))
    description = forms.CharField(widget=forms.Textarea(attrs=FieldsAttrs.description))
    # images = forms.Field(widget=forms.ClearableFileInput(attrs=FieldsAttrs.images), required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True,
                                      widget=forms.Select(attrs=FieldsAttrs.category))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.product = None
        super(ExposeProductForm, self).__init__(*args, **kwargs)

    def save(self):
        cleaned_data = self.cleaned_data
        product_data = {}
        for key in ('title', 'price', 'description', 'category'):
            item = cleaned_data.get(key)
            if item:
                product_data[key] = item
        product_data['seller'] = self.request.user
        product = Product(**product_data)
        product.save()
        self.product = product
        return product

    def clean(self):
        print('form clean#', self.cleaned_data)
        return self.cleaned_data
