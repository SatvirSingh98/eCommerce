from decimal import Decimal as D

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.addresses.models import Address
from apps.billing.models import BillingProfile
from apps.cart.models import Cart
from eCommerce.utils import unique_order_id_generator

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
    ('cancelled', 'Cancelled'),
    ('delivered', 'Delivered')
)


class OrderManager(models.Manager):
    def create_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True, status='created')
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.get_queryset().create(cart=cart_obj, billing_profile=billing_profile)
            created = True
        return obj, created


class Order(models.Model):
    order_id = models.CharField(max_length=50, blank=True)

    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.CASCADE)

    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='shipping_address',
                                         null=True, blank=True,)

    billing_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='billing_address',
                                        null=True, blank=True)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)

    shipping_charges = models.DecimalField(default=0.00, max_digits=65, decimal_places=2)

    total = models.DecimalField(default=0.00, max_digits=65, decimal_places=2)

    active = models.BooleanField(default=True)

    objects = OrderManager()

    def __str__(self):
        return f'{self.cart} - {self.order_id}'

    def update_total(self):
        self.total = D(self.cart.total) + D(self.shipping_charges)
        self.save()
        return self.total

    def checkout_success(self):
        if self.billing_profile and self.shipping_address and self.billing_address and self.total:
            return True
        return False

    def order_paid(self):
        if self.checkout_success():
            self.status = 'paid'
            self.save()
        return self.status


@receiver(pre_save, sender=Order)
def order_id_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


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
