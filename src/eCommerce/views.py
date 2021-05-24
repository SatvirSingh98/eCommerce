from django.shortcuts import redirect, render

from .forms import ContactForm


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
        form = ContactForm()
        return redirect('.')
    return render(request, 'contact/view.html', {'form': form})
