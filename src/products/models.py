import uuid

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class ProductManager(models.Manager):

    def category(self, title):
        queryset = self.get_queryset().filter(category__title=title)
        return queryset


class Product(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=False, blank=False)
    description = models.TextField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('products.Category', null=True, on_delete=models.SET_NULL)

    objects = ProductManager()

    def __str__(self):
        return str(self.title) + ' ' + str(self.seller.email)


def build_image_upload_path(instance, filename):
    old_name = ext = filename.rsplit('.', 1)
    new_name = str(uuid.uuid1())
    return '/products/images/' + new_name + '.' + ext


class Image(models.Model):
    image = models.ImageField(upload_to=build_image_upload_path)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.image.url)


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return str(self.title)
