from django.shortcuts import render


def home(request):
    cart_id = request.session.get('cart_id', None)
    if cart_id is None:
        print('Create new cart')
        request.session['cart_id'] = 12
    else:
        print('Cart id exists')
    return render(request, 'cart/home.html', {'cart_id': cart_id})
