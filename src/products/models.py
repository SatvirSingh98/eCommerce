import os
from django.db import models


##############################################################
# advanced way to create filename to avoid errors this is for small files.
# Note: Do not use this method for large files instead use service like aws.
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    print(os.path.splitext(base_name))
    name, ext = os.path.splitext(base_name)
    return name, ext


def image_upload_path(instance, filename):
    print(instance)
    print(filename)
    name, ext = get_filename_ext(filename)
    new_filename = f"{instance}{ext}"
    return f"products/{instance}/{new_filename}"
##############################################################


##############################################################
# creating custom model manager
class ProductManager(models.Manager):
    def get_by_id(self, pk):
        qs = self.get_queryset().filter(pk=pk)
        # self.get_queryset() = Product.objects

        return qs.first() if qs.count() == 1 else None

    def get_featured(self):
        return self.get_queryset().filter(featured=True)
##############################################################


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    image = models.ImageField(
        upload_to=image_upload_path, null=True, blank=True)
    featured = models.BooleanField(default=False)

    # this is not overriding defaults, instead extending it's functionality.
    objects = ProductManager()

    def __str__(self):
        return self.title
