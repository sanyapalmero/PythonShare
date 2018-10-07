from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from . import forms
from django.http import HttpResponse
from . import models


# Create your views here.
class CreateView(View):
    def get(self, request):
        form = forms.UserForm()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = forms.UserForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        repeat_password = request.POST['repeat_password']
        if form.is_valid():
            user = models.User.objects.create_user(username, password)
            good = 'Вы успешно зарегистрированы!'
            return render(request, 'user/register.html', {
                'form': form,
                'good': good
            })
        else:
            return render(request, 'user/register.html', {'form': form})
