from django import forms


class TextForm(forms.Form):
    textfield = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'style': 'height:200px'
        }),
        label="Создание текстового документа",
        max_length=100)
