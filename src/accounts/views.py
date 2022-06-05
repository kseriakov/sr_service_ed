from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import *


def login_view(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email = data.get('email')
            password = data.get('password')
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = form.save(commit=False)
            new_user.set_password(data.get('password'))
            new_user.save()
            if new_user:
                return render(request, 'accounts/register_success.html', {'new_user': new_user})
            else:
                form.errors.set_default('create_user_error', 'Ошибка регистрации, введите корректные данные')

    return render(request, 'accounts/register.html', {'form': form})


def update_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateSettings(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data.get('city')
                user.language = data.get('language')
                user.send_mail = data.get('send_mail')
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Настройки личного кабинета успешно сохранены!')
            return redirect('home')

        else:
            form = UserUpdateSettings(instance=user)
    else:
        return redirect('accounts:login')

    return render(request, 'accounts/update_settings.html', {'form': form})


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            u = get_user_model().objects.get(pk=user.pk)
            u.delete()
            messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
            return redirect('home')
