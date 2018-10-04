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


class AddView(View):
    def post(self, request):
        form = forms.UserForm()
        username = request.POST['username']
        password = request.POST['password']
        repit_password = request.POST['repit_password']
        if password == repit_password:
            try:
                user = get_object_or_404(models.User, username=username)
                error = "Пользователь с этим именем уже существует!"
                return render(request, 'user/register.html', {
                    'form': form,
                    'error': error
                })
            except:
                user = models.User.objects.create_user(username, password)
                good = "Вы успешно зарегестрированы!"
                return render(request, 'user/register.html', {
                    'form': form,
                    'good': good
                })
        else:
            error = "Пароли не совпадают!"
            return render(request, 'user/register.html', {
                'form': form,
                'error': error
            })
        #redirect to main page
        return HttpResponse('nice')
