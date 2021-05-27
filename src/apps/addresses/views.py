from django.shortcuts import redirect
from django.utils.http import is_safe_url

from apps.billing.models import BillingProfile

from .forms import AddressForm


def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)

    # for redirecting after login
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post

    if form.is_valid():
        print(request.POST)
        instance = form.save(commit=False)
        billing_profile, _ = BillingProfile.objects.create_or_get(request)

        if billing_profile is not None:
            instance.billing_profile = billing_profile
            instance.address_type = request.POST.get('address_type', 'shipping')
            instance.save()
        else:
            print('error')
            return redirect('cart:checkout')

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('cart:checkout')
    return redirect('cart:checkout')
