from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.products.models import Product
from eCommerce.utils import unique_slug_generator


# Create your models here.
class ProductTag(models.Model):
    products = models.ManyToManyField(Product, blank=True)
    title = models.CharField(max_length=120)
    slug = models.SlugField(null=True, blank=True, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


@receiver(pre_save, sender=ProductTag)
def tag_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
