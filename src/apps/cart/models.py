from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver

from apps.products.models import Product

User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_cart(self, user=None):
        user_obj = None
        if user is not None and user.is_authenticated:
            user_obj = user
        return self.get_queryset().create(user=user_obj)

    def create_or_get(self, request):
        cart_id = request.session.get('cart_id')
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            created = False
            cart_obj = qs.first()

            # below will set the current session cart to the user if he is authenticated and of the same session.
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            # below line will return guest or authenticated user.
            # if user is not authenticated it will return 'AnonymousUser' and create() will give an error.
            cart_obj = self.new_cart(user=request.user)
            created = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, created


class Cart(models.Model):
    # Any user can make cart, so null and blank are True
    # because session can be for both logged in and not logged in user.
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    # for blank cart blank is True
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(decimal_places=2, max_digits=65, default=0.00)
    subtotal = models.DecimalField(decimal_places=2, max_digits=65, default=0.00)
    tax = models.DecimalField(default=18.00, max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


# m2m_changed is used because of ManyToManyField
@receiver(m2m_changed, sender=Cart.products.through)
def cart_m2m_changed_reciever(sender, action, instance, *args, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        products = instance.products.all()
        subtotal = 0
        for item in products:
            subtotal += item.price

        if instance.subtotal != subtotal:
            instance.subtotal = subtotal
            instance.save()


# pre_save is used to change the total amount based on subtotal
@receiver(pre_save, sender=Cart)
def cart_pre_save_reciever(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        tax = instance.subtotal * (instance.tax * Decimal('0.01'))
        instance.total = instance.subtotal + tax
    else:
        instance.total = 0.00
