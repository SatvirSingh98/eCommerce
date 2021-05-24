from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import redirect, render
from django.utils.http import is_safe_url

from .forms import LoginForm, RegisterForm

User = get_user_model()


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

        user = User(username=username, password=password, email=email)
        user.set_password('password')
        user.save()
        form = RegisterForm()
        return redirect('login')

    return render(request, 'accounts/register.html', {'form': form})
