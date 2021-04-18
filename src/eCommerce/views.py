from django.contrib.auth import authenticate, get_user_model, login
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse

from .forms import ContactForm, LoginForm, RegisterForm

User = get_user_model()


def index(request):
    context = {
        'title': 'Hello World',
        'content': 'Welcome to home page'
    }
    if request.user.is_authenticated:
        context['user'] = request.user.username
    return render(request, 'index.html', context)


def about_page(request):
    context = {
        'content': 'Welcome to about page'
    }
    return render(request, 'index.html', context)


def contact_page(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        form = ContactForm()
        return redirect('.')
    return render(request, 'contact/view.html', {'form': form})


def login_page(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                form = LoginForm()
                return redirect(reverse('index'))
        else:
            return HttpResponse('Your account is inactive')
    return render(request, 'auth/login.html', {'form': form})


def register_page(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        User.objects.create_user(username=username, password=password,
                                 email=email)
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})
