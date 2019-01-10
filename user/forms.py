from django import forms

from . import models


class CreateUserForm(forms.Form):
    username = forms.CharField(label="Имя пользователя", max_length=20)
    password = forms.CharField(label="Пароль", max_length=128)
    repeat_password = forms.CharField(label="Повторите пароль", max_length=128)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = models.User.objects.get(username=username)
            error = 'Пользователь с таким именем уже существует!'
            self.add_error('username', error)
        except models.User.DoesNotExist:
            return username

    def clean(self):
        cleaned_data = super().clean()
        password = self.data.get('password')
        repeat_password = self.data.get('repeat_password')
        if password != repeat_password:
            error = 'Пароли не совпадают!'
            self.add_error('password', error)
            self.add_error('repeat_password', error)
        else:
            return cleaned_data


class LoginUserForm(forms.Form):
    username = forms.CharField(label="Ваше имя", max_length=20)
    password = forms.CharField(label="Пароль", max_length=128)
