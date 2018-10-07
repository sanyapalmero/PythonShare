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
