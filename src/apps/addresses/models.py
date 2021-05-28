from django.db import models

from apps.billing.models import BillingProfile

ADDRESS_TYPE = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping')
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=50, choices=ADDRESS_TYPE)
    address_line1 = models.CharField(max_length=150)
    address_line2 = models.CharField(max_length=150, null=True, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        return "{line1} {line2}, {city}, {state}, {country}, {postal_code}".format(
            line1=self.address_line1, line2=self.address_line2 or '', city=self.city,
            state=self.state, country=self.country, postal_code=self.postal_code
        )
