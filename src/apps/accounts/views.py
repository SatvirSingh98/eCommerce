from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import redirect, render
from django.utils.http import is_safe_url

from .forms import LoginForm, RegisterForm

User = get_user_model()


def login_excluded(redirect_to):
    """ This decorator is to prevent visiting the login_page after the user is authenticated """
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper


@login_excluded('/')
def login_page(request):
    form = LoginForm(request.POST or None)

    # for redirecting after login
    next_ = request.GET.get('next')
    # eg: 127.0.0.1/accounts/login/?next=<your redirect url>

    next_post = request.POST.get('next')
    redirect_path = next_ or next_post

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            form = LoginForm()

            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')
        else:
            print('Error')
    return render(request, 'accounts/login.html', {'form': form})


def register_page(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')

        User.objects.create_user(username=username, password=password, email=email)
        form = RegisterForm()
        return redirect('accounts:login')

    return render(request, 'accounts/register.html', {'form': form})
