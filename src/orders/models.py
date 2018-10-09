from django.contrib.auth import get_user_model
from django.db import models

from products.models import Product

User = get_user_model()


class Order(models.Model):

    product = models.OneToOneField(Product, null=True, on_delete=models.SET_NULL)
    buyer = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    datetime = models.DateTimeField(auto_created=True, editable=False)
