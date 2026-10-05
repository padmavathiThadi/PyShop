from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('index')

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {
        'form': form
    })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_url = request.POST.get('next')

            if next_url:
                return redirect(next_url)

            return redirect('index')

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {
        'form': form,
        'next': request.GET.get('next', '')
    })


def logout_view(request):
    logout(request)

    return redirect('index')