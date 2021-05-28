from django.shortcuts import redirect
from django.utils.http import is_safe_url

from apps.addresses.models import Address
from apps.billing.models import BillingProfile

from .forms import AddressForm


def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)

    # for redirecting after filling address
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post

    if form.is_valid():
        instance = form.save(commit=False)
        billing_profile, _ = BillingProfile.objects.create_or_get(request)

        if billing_profile is not None:
            address_type = request.POST.get('address_type', 'shipping')
            instance.billing_profile = billing_profile
            instance.address_type = address_type
            instance.save()
            request.session[address_type + '_address_id'] = instance.id
        else:
            print('error')
            return redirect('cart:checkout')

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
    return redirect('cart:checkout')


def checkout_address_reuse_view(request):
    if request.user.is_authenticated:
        # for redirecting after selecting address
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post

        if request.method == 'POST':
            print(request.POST)
            address = request.POST.get('address')
            address_type = request.POST.get('address_type', 'shipping')
            billing_profile, _ = BillingProfile.objects.create_or_get(request)

            if address is not None:
                qs = Address.objects.filter(billing_profile=billing_profile, id=address)
                if qs.exists():
                    request.session[address_type + '_address_id'] = address
                    if is_safe_url(redirect_path, request.get_host()):
                        return redirect(redirect_path)
    return redirect('cart:checkout')
