from django import forms


class UserForm(forms.Form):
    username = forms.CharField(
        label="Имя пользователя",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width:250px'
        }))
    password = forms.CharField(
        label="Пароль",
        max_length=128,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width:250px',
            'type': 'password'
        }))
    repit_password = forms.CharField(
        label="Повторите пароль",
        max_length=128,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width:250px',
            'type': 'password'
        }))
