from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import GuestEmail

User = settings.AUTH_USER_MODEL


class BillingProfileManager(models.Manager):
    def create_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if user.is_authenticated:
            obj, created = self.model.objects.get_or_create(user=user, email=user.email)
        elif guest_email_id is not None:
            guest_email = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(email=guest_email)
            created = True
        return obj, created


# we want to create billing profile when the user is created.
class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = BillingProfileManager()

    def __str__(self):
        if self.user_id:
            return f'Registered User - {self.email}'
        return f'Guest - {self.email}'


# We want to create the billing profile when user is created, so post_save is used.
@receiver(post_save, sender=User)
def user_created_reciever(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        # instance = username
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)
