from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = settings.AUTH_USER_MODEL


# we want to create billing profile when the user is created.
class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


# We want to create the billing profile when user is created, so post_save is used.
@receiver(post_save, sender=User)
def user_created_reciever(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        # instance = username
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)
