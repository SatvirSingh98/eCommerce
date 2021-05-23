from django.conf import settings
from django.db import models

from apps.products.models import Product

User = settings.AUTH_USER_MODEL


class Cart(models.Model):
    # Any user can make cart, so null and blank are True
    # because session can be for both logged in and not logged in user.
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    # for blank cart blank is True
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(decimal_places=2, max_digits=65, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
