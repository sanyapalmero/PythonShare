from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from . import forms
from django.http import HttpResponse
from . import models
from django.contrib.auth import authenticate, login, logout


# Create your views here.
class CreateView(View):
    def get(self, request):
        form = forms.CreateUserForm()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            user = models.User.objects.create_user(username, password)
            good = 'Вы успешно зарегистрированы!'
            return render(request, 'user/register.html', {
                'form': form,
                'good': good
            })
        else:
            return render(request, 'user/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('text:index')
        else:
            bad = 'Неверное имя пользователя или пароль'
            return render(request, 'user/login.html', {'bad': bad})


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect('text:index')
