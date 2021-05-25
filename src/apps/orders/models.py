from decimal import Decimal as D

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.cart.models import Cart
from eCommerce.utils import unique_order_id_generator

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
    ('cancelled', 'Cancelled')
)


class Order(models.Model):
    order_id = models.CharField(max_length=50, blank=True)
    # billing_profile
    # shipping_address
    # billing_address
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_charges = models.DecimalField(default=0.00, max_digits=65, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=65, decimal_places=2)

    def __str__(self):
        return f'{self.cart} - {self.order_id}'

    def update_total(self):
        self.total = D(self.cart.total) + D(self.shipping_charges)
        self.save()
        return self.total


@receiver(pre_save, sender=Order)
def order_id_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


@receiver(post_save, sender=Cart)
def cart_total_post_save_reciever(sender, instance, created, *args, **kwargs):
    if not created:
        qs = Order.objects.filter(cart__id=instance.id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


@receiver(post_save, sender=Order)
def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


@receiver(pre_save, sender=Order)
def shipping_pre_save_reciever(sender, instance, *args, **kwargs):
    if instance.shipping_charges > 0:
        instance.total = D(instance.shipping_charges) + D(instance.cart.total)
    else:
        instance.total = instance.cart.total
